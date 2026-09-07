# Document OCR into the ERP: supplier bills and expense claims read automatically

## Situation
A manufacturing group with six sites, buying from suppliers in several countries, with staff submitting expense claims from all of them. Every one of those documents ends up as a record in the ERP. Until recently, every one got there because a person typed it.

## Business problem
Data entry was the bottleneck between a document arriving and the business knowing about it. A supplier bill sat in a mailbox or a tray until somebody had time, so the payables position was always a few days behind reality. Expense claims were worse, because they arrive as photographs of receipts in whatever condition the person's pocket left them.

## My responsibility
I designed and built it. This is one of five AI systems of my own design running in daily production at the group, not a proof of concept and not a vendor product I bought and configured.

## Solution
A pipeline that reads the document and creates the record in the ERP. A bill or a claim arrives, the pipeline extracts the fields that matter, and an ERP record appears with those values populated and the original document attached.

The design principle I held to is that the pipeline creates records, it does not post to the ledger on its own. Extraction is not perfect, and a language model is confidently wrong in a way a broken scanner never is. So the output lands where the group's existing controls already apply. Vendor bills continue through the approval workflow I had already built into the ERP, where a rejected bill carries a recorded reason and a non-standard payment term is a request with an approver. Finance changed from typing values to checking them.

## Technology
Gemini and Claude vision APIs, Python, Odoo, PostgreSQL.

## Implementation
Built against the group's own document mix rather than clean samples, because the real population determines whether this works. Wired into the existing bill and expense models, so documents follow the approval path that was already there.

## Challenges
Supplier documents have no common layout. Every supplier invoices differently, in different languages, and the same supplier changes its template without telling anyone. The engineering problem is less about reading characters than about deciding which number on an unfamiliar page is the one you want, and being honest about what the system should refuse to guess at.

## Result
Documents are processed on arrival rather than waiting for somebody to be at a desk, with the original attached to the record. Finance reviews and approves instead of transcribing.

## Verified evidence
The pipeline runs in daily production against live supplier bills and expense claims. Its output lands in the ERP bill and expense models I built, in the custom module tree I hold, alongside the payment-term request and bill-rejection workflows it feeds. I work in this space commercially as well, having specified a document OCR product under my own venture. I hold the pipeline logs and can produce the processed-document count and date range on request. I do not quote a figure I have not measured.

## Skills demonstrated
Applied AI in production, vision and language model APIs, Python engineering, ERP integration, process redesign in finance, judgement about where automation should stop.

## Suitable target roles
Head of Digital and AI Transformation, IT Director, Senior Leader IT and AI Transformation, ERP Manager.

## Three interview talking points
1. "Supplier bills and expense claims are read by an OCR pipeline and land in the ERP as records. It runs in production, not as a trial."
2. "It creates the record, it does not post the entry. A model is confidently wrong in a way a scanner never is, so finance checks rather than types."
3. "The hard part was never character recognition. It is deciding which number on an unfamiliar layout is the one you want."
