---
title: "Reading supplier bills into an ERP with an LLM OCR pipeline: a design that survives production"
description: Design a supplier bill OCR pipeline with a vision model, strict JSON, validation rules, a review queue, idempotency and honest monthly accuracy checks.
date: 2026-09-08
modified: 2026-09-10
type: tutorial
tags: [ai, ocr, erp, accounts-payable]
---

# Reading supplier bills into an ERP with an LLM OCR pipeline: a design that survives production

By the end of this you will have a design for a pipeline that takes supplier bills from wherever they arrive, reads them with a vision-capable model, checks the result against rules finance would apply, and creates a draft bill in the ERP or hands it to a person. It is for IT heads and engineers building this in-house.

## What you need

- A vision-capable model with an API, such as Gemini or Claude, and a budget for it
- Python 3.11 or later and a PDF renderer (`pdftoppm` or PyMuPDF)
- Read access to the bill sources: mailbox, scanner share, WhatsApp Business account
- An ERP API for creating draft vendor bills (Odoo's `account.move` in my case)
- Two tables of your own: an audit log and a hash register
- A finance person who will label a sample of bills by hand

I run a pipeline of this shape in production. What follows is the design, not the code, and each rule is here because it caught something.

## The shape of it

Capture, extract, validate, route, record, measure. One principle holds the six stages together: the pipeline creates draft records, it does not post to the ledger. A model is confidently wrong in a way a broken scanner never is. The output lands where your existing approval controls already apply, and finance changes from typing values to checking them.

## 1. Capture

Three sources cover most companies: a dedicated mailbox read by IMAP or the Gmail API, a watched folder where the scanner drops PDFs, and the WhatsApp Business API webhook, because suppliers in some markets send bills as phone photographs and will not stop.

Each source produces the same thing: a file, a source tag, a sender identity if there is one, and a timestamp. Store the original bytes before anything else; you need them for the audit trail, for reprocessing when the prompt improves, and for the argument with a supplier about what their bill said. Then compute a SHA-256 of the bytes and check it against your register.

## 2. Extraction against a strict schema

Render each page to an image (150 to 200 dpi; more costs money and reads no better), send every page in one request, and ask for JSON only against a schema you include in the prompt, with the API's structured output mode if it has one and the temperature at zero. Validate the response against the schema in code before anything else looks at it; a response that does not parse is a failure, not a partial success.

The schema I use is close to this:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["document_type", "supplier", "invoice_number", "invoice_date",
               "currency", "lines", "subtotal", "tax_total", "total",
               "handwritten_amendments", "unreadable_fields"],
  "properties": {
    "document_type": {"enum": ["invoice", "credit_note", "statement", "proforma", "other"]},
    "supplier": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": {"type": "string"},
        "tax_id": {"type": ["string", "null"]}
      }
    },
    "invoice_number": {"type": "string"},
    "invoice_date": {"type": "string", "format": "date"},
    "currency": {"type": "string", "pattern": "^[A-Z]{3}$"},
    "lines": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["description", "quantity", "unit_price", "amount"],
        "properties": {
          "description": {"type": "string"},
          "quantity": {"type": "number"},
          "unit_price": {"type": "number"},
          "tax_rate": {"type": ["number", "null"]},
          "amount": {"type": "number"}
        }
      }
    },
    "subtotal": {"type": "number"},
    "tax_total": {"type": "number"},
    "total": {"type": "number"},
    "handwritten_amendments": {"type": "boolean"},
    "unreadable_fields": {"type": "array", "items": {"type": "string"}}
  }
}
```

Two fields do most of the work. `document_type` lets the model say that the thing in the mailbox is a statement or a pro forma, which is not a bill and must not become one. `unreadable_fields` lets it say "I could not read the total" instead of guessing. Tell it in the prompt, in plain words, that a guessed number is worse than naming the field as unreadable; that one instruction removed more bad records than any clever prompting. Dates are ISO so the model makes the day-month decision once, and numbers are numbers, so "1.234,56" and "1,234.56" both arrive as 1234.56.

## 3. Validation rules

The schema proves the shape; the rules prove the content. Each rule yields a named pass or fail with a detail string for the reviewer.

```python
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

TOLERANCE = Decimal("0.05")


@dataclass
class Check:
    name: str
    passed: bool
    detail: str = ""


def money(value) -> Decimal:
    return Decimal(str(value))


def validate(doc: dict, vendors, register, today: date) -> list[Check]:
    checks = []
    lines_sum = sum(money(line["amount"]) for line in doc["lines"])
    subtotal, tax, total = money(doc["subtotal"]), money(doc["tax_total"]), money(doc["total"])

    checks.append(Check("is_invoice", doc["document_type"] in ("invoice", "credit_note"),
                        doc["document_type"]))
    checks.append(Check("lines_add_up", abs(lines_sum - subtotal) <= TOLERANCE,
                        f"lines {lines_sum} vs subtotal {subtotal}"))
    checks.append(Check("total_adds_up", abs(subtotal + tax - total) <= TOLERANCE,
                        f"{subtotal} + {tax} vs {total}"))
    checks.append(Check("nothing_unreadable", not doc["unreadable_fields"],
                        ", ".join(doc["unreadable_fields"])))
    checks.append(Check("no_handwriting", not doc["handwritten_amendments"]))

    vendor = vendors.match(doc["supplier"]["name"], doc["supplier"].get("tax_id"))
    checks.append(Check("supplier_in_master", vendor is not None, doc["supplier"]["name"]))
    if vendor:
        number = doc["invoice_number"].strip().upper()
        checks.append(Check("invoice_number_unique",
                            not register.exists(vendor.id, number), number))
        checks.append(Check("currency_expected", doc["currency"] in vendor.currencies,
                            doc["currency"]))

    age = (today - date.fromisoformat(doc["invoice_date"])).days
    checks.append(Check("date_plausible", 0 <= age <= 365, doc["invoice_date"]))
    return checks
```

The supplier match deserves care: tax registration number first, then a normalised name, and a weak name-only match is a fail. A spelling difference between the bill and the vendor master is a matching problem to solve in code, not a reason to create a vendor. Invoice number uniqueness is per supplier, because two suppliers can both issue "INV-1001"; the register holds (vendor, normalised number) pairs written when a bill is created, and it catches a second scan of the same bill even when the file bytes differ.

## 4. Confidence and the review queue

Do not ask the model how confident it is and route on the answer; the number is not calibrated, and I have watched it report high confidence on a total it invented. Confidence here is earned three ways: every rule passed, a second extraction (a different rendering or a second model) agrees on supplier, number, date and total, and the supplier has a history of clean extractions.

Anything that fails a rule or disagrees on a key field goes to the review queue, with the page images, the JSON and the failed checks side by side. Start with everything reviewed until the measurement in step 8 says the straight-through path is safe, then loosen one supplier at a time.

Record every correction a reviewer makes; corrections are evidence for the accuracy figure and raw material for better rules.

## 5. Idempotency and the audit log

The same bill arrives twice more often than you would think: forwarded by two people, sent by supplier and buyer, rescanned because the first looked crooked. The file hash catches byte-identical repeats before you spend anything, the register catches repeats that are different files, and for email the message ID is a third key. The register needs a status column, because a bill waiting in review is not yet in the ERP and a second copy must be tied to the first.

The audit log is one row per document per attempt: hash, source and sender, received time, model and prompt version, the raw JSON, every check with its result, the route taken, the ERP record created, the reviewer's decision and corrections, and a timestamp for each step. When someone asks in six months why a bill went in with the wrong total, this is the only thing that answers them.

## 6. Cost control

Vision models charge roughly by the page. Cap pages per document (the first few and the last; a twenty-page bill is usually a statement with a bill stapled to it, and anything over the cap goes to review). Send downscaled JPEGs, not full-resolution PNGs. Batch non-urgent sources overnight if the API has a cheaper batch tier. Set a daily spend ceiling with an alert and a hard stop above it.

## 7. Failure modes I have met

Handwritten amendments: a printed total with a pen correction beside it. The model reads the printed number, so the `handwritten_amendments` flag sends these to review.

Multi-page bills: a subtotal on page two gets read as the total. Sending every page in one request fixes most of it; the totals rule catches the rest.

Stamps over numbers: a "RECEIVED" stamp across the total, or a signature through the invoice number. The model guesses at the hidden digits, the second extraction disagrees, and it goes to review.

Duplicates: covered above, except a supplier reissuing a corrected bill under the same number, which the register flags for a reviewer to decide.

## 8. Measuring accuracy honestly

An accuracy figure from a demo is worthless; measure on your own document mix. Each month, draw a random sample of processed bills (a hundred is a workable size), straight-through and reviewed alike. A finance person keys the fields from the original without seeing the pipeline's output. Compare field by field and report three numbers: accuracy per key field, the straight-through rate (bills needing no human touch), and the rate at which straight-through bills were later found wrong. That third number is the one that matters and the one nobody publishes.

Track it by supplier, because suppliers change templates without telling anyone and accuracy drops one supplier at a time. Do not use the reviewers' corrected values as ground truth; a reviewer can accept a wrong value that looked right.

## Common questions

### Why not a template-based OCR product instead of a language model?

Templates work when your suppliers are few and their layouts stable. Mine are neither: every supplier invoices differently, in more than one language, and changes its template without warning. A vision model reads an unfamiliar layout on the first attempt, and the rules above decide whether to trust what it read.

### Should the pipeline create the vendor when it cannot find one?

No. A vendor record is a control point: someone checked the trade licence, the tax registration and the bank details before it existed. Route the bill to review as "supplier not found", let a person create the vendor through the normal path, and reprocess it.

### How do I keep the model from inventing line items on a bill that has none?

Say in the prompt that some bills carry only a total and an empty `lines` array is the right answer for them. Invented lines rarely add up to the printed subtotal, so `lines_add_up` fails and the reviewer sees the empty page next to the invented rows.
