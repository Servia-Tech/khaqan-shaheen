---
title: "Reading supplier bills into an ERP with an LLM OCR pipeline: a design that survives production"
description: Design a supplier bill OCR pipeline with a vision model, strict JSON, validation rules, a review queue, idempotency and honest monthly accuracy checks.
date: 2026-09-08
type: tutorial
tags: [ai, ocr, erp, accounts-payable]
---

# Reading supplier bills into an ERP with an LLM OCR pipeline: a design that survives production

By the end of this you will have a design for a pipeline that takes supplier bills from wherever they arrive, reads them with a vision-capable model, checks the result against rules your finance team would apply, and creates a draft bill in the ERP or hands it to a person. It is for IT heads and engineers building this for their own company.

## What you need

- A vision-capable model with an API, such as Gemini or Claude, and a budget for it
- Python 3.11 or later, with a PDF renderer (`pdftoppm` from poppler, or PyMuPDF)
- Read access to the bill sources: a mailbox, a scanner share, a WhatsApp Business account
- An ERP with an API for creating draft vendor bills (Odoo's `account.move` over JSON-RPC in my case)
- A table or two of your own for the audit log and the hash register
- A finance person who will label a sample of bills by hand, monthly

I run a pipeline of this shape in production. What follows is the design, not the code, and each rule is here because it caught something.

## The shape of it

Six stages, each with one job:

1. Capture: collect the file and a record of where it came from
2. Extract: the model reads the pages and returns JSON that matches a schema
3. Validate: rules decide whether the JSON is trustworthy
4. Route: trusted results become draft bills, the rest go to a review queue
5. Record: every step writes to an audit log
6. Measure: a labelled sample tells you how accurate it is

The principle that holds it together: the pipeline creates draft records, it does not post to the ledger. A model is confidently wrong in a way a broken scanner never is. The output lands where your existing approval controls already apply, and finance changes from typing values to checking them.

## 1. Capture

Three sources cover most companies. A mailbox (a dedicated address read by IMAP or the Gmail API, keeping every attachment and the message ID). A scanner folder (a watched share where the multi-function device drops PDFs). WhatsApp (the Business API webhook, because suppliers in some markets send bills as photographs from a phone and will not stop).

Each source produces the same thing: a file, a source tag, a sender identity if there is one, and a received timestamp. Store the original bytes before you do anything else. You need them for the audit trail, for reprocessing when you improve the prompt, and for the argument with a supplier about what their bill said.

Compute a SHA-256 of the bytes here and check it against your register. This is the first idempotency guard, and it sits before the model call so a repeat costs nothing.

## 2. Extraction against a strict schema

Render each page to an image (150 to 200 dpi is enough; more costs money and does not read better), send all the pages in one request, and ask for JSON only, against a schema you include in the prompt. Use the API's structured output or JSON mode if it has one, and set the temperature to zero. Then validate the response against the schema in code before anything else looks at it. A response that does not parse is a failure, not a partial success.

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
        "tax_id": {"type": ["string", "null"]},
        "country": {"type": ["string", "null"]}
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

Two fields do most of the work. `document_type` lets the model tell you that the thing in the mailbox is a statement or a pro forma, which is not a bill and must not become one. `unreadable_fields` gives the model a way to say "I could not read the total" instead of guessing. Tell it in the prompt, in plain words, that a guessed number is worse than naming the field as unreadable. That one instruction removed more bad records than any clever prompting.

Dates are ISO in the schema so the model makes the day-month decision once, with the supplier's country as a hint. Numbers are numbers, so "1.234,56" and "1,234.56" both arrive as 1234.56.

## 3. Validation rules

The schema proves the shape. The rules prove the content. Every rule produces a named pass or fail with a detail string, because the review queue shows those to the reviewer.

```python
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

TOLERANCE = Decimal("0.05")   # rounding across tax lines


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

The supplier match deserves care. Match on tax registration number first, then on a normalised name, and treat a name-only match below a similarity threshold as a fail. The vendor master is the only place the pipeline learns supplier names from. If the model reads "Al Something Trading LLC" and your master says "Al Something Trading L.L.C.", that is a matching problem for you to solve in code, not a reason to create a vendor.

Invoice number uniqueness is per supplier, not global. Two suppliers can both issue "INV-1001". The register is a table of (vendor, normalised number) pairs written when a bill is created, and it catches the second scan of the same bill even when the file bytes differ.

## 4. Confidence and the review queue

Do not ask the model how confident it is and route on the answer. The number it gives you is not calibrated, and I have watched it report high confidence on a total it invented. Confidence in this pipeline is earned three ways:

- Every validation rule passed
- A second extraction agrees: run the same pages again (a different rendering, or a second model) and compare supplier, number, date and total
- The supplier has a history of clean extractions

Anything that fails a rule or disagrees on a key field goes to the review queue, with the page images, the JSON and the failed checks side by side. Start with everything reviewed, including the passes, until the measurement in step 8 says the straight-through path is safe. Loosen from there, one supplier at a time.

The review queue is a screen your finance team will live in, so build it for them: keyboard-driven, the failed rule at the top, one key to accept, one to correct a field, one to reject with a reason. Every correction is recorded, because corrections are evidence for your accuracy figure and the raw material for better rules.

## 5. Idempotency and the audit log

The same bill arrives twice more often than you would think: forwarded by two people, sent by the supplier and again by the buyer, scanned again because the first scan looked crooked. Two guards, in order:

1. The file hash from step 1 catches byte-identical repeats before you spend anything on them
2. The (vendor, invoice number) register catches repeats that are different files

For email, keep the message ID as a third key. The register needs a status column, because a bill sitting in the review queue is not yet in the ERP, and a second copy arriving while it waits must be tied to the first, not treated as new.

The audit log is one row per document per attempt: the hash, the source and sender, the received time, the model and prompt version, the raw JSON returned, every check with its result, the route taken, the ERP record created if any, the reviewer's decision and corrections, and the timestamp of each step. When someone asks in six months why a bill went in with the wrong total, this is the only thing that answers them.

## 6. Cost control

Vision models charge roughly by the page. The controls that matter:

- A page cap per document, the first few pages and the last one, because a bill with twenty pages is usually a statement with a bill stapled to it; anything over the cap goes to review with a note
- Downscaled JPEG pages rather than full-resolution PNGs
- The hash check before the model call, not after
- Batching non-urgent sources overnight if the API offers a cheaper batch tier
- A daily spend ceiling with an alert, and a hard stop above it

## 7. Failure modes I have met

Handwritten amendments. A printed total with a pen correction beside it, or a handwritten discount at the bottom. The model reads the printed number. The `handwritten_amendments` flag sends these to review.

Multi-page bills. Line items run across pages, and a subtotal on page two gets read as the total. Sending all pages in one request fixes most of it; the totals rule catches the rest.

Stamps over numbers. A "RECEIVED" or "PAID" stamp across the total, or a signature through the invoice number. The model guesses at the obscured digits. The totals rule and the second extraction disagree, and it goes to review.

Duplicates sent twice. Covered above, but the case that still needs a person is a supplier who reissues a corrected bill under the same number. The register flags it and a reviewer decides, which is the right outcome.

Statements and pro formas. `document_type` and the `is_invoice` rule keep them out of accounts payable.

Foreign currency and thousands separators. Give the model the supplier's country and expected currency as hints, and let `currency_expected` catch the rest.

## 8. Measuring accuracy honestly

An accuracy figure from a demo is worthless. Measure on your own document mix.

Each month, draw a random sample of processed bills (a hundred is a workable size), including ones that went straight through and ones that were reviewed. A finance person keys the fields from the original document without seeing the pipeline's output. Compare field by field. Report three numbers: accuracy for each key field, the straight-through rate (bills that needed no human touch), and the rate at which straight-through bills were later found to be wrong. That third number is the one that matters and the one nobody publishes.

Track it by supplier, because suppliers change their templates without telling anyone and accuracy drops one supplier at a time. Do not use the reviewers' corrected values as ground truth; a reviewer can accept a wrong value that looked right. The monthly re-check is what makes the number believable a year later.

## Common questions

### Why not a template-based OCR product instead of a language model?

Templates work when your suppliers are few and their layouts stable. Mine are neither: every supplier invoices differently, in more than one language, and the same supplier changes its template without warning. A vision model reads an unfamiliar layout on the first attempt, and the rules above do the job the template used to do, which is deciding whether to trust what was read.

### Should the pipeline create the vendor when it cannot find one?

No. A vendor record is a control point: someone checked the trade licence, the tax registration and the bank details before it existed. Let the pipeline route the bill to review with a "supplier not found" reason, and let a person create the vendor through the normal path. The bill is then reprocessed and matches.

### How do I keep the model from inventing line items on a bill that has none?

Say so in the prompt: some bills carry only a total, and an empty `lines` array is the correct answer for them. Then let the rules do their work. Invented lines rarely add up to the printed subtotal, so `lines_add_up` fails and the bill goes to review, where the reviewer sees the empty page next to the invented rows.
