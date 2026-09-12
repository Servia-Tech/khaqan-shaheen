# Five AI systems in daily production at a UAE plastics manufacturer

## Situation
A plastics manufacturing group in the UAE with six sites in five countries, four brands and four websites, around 150 users, and one Odoo ERP that every site works from. I am Head of IT, reporting directly to the owner. AI was not a project the business asked for. It came out of watching where people's hours went: retyping supplier bills, checking documents by eye, answering the same enquiries at midnight, and phones ringing out after hours.

## Business problem
Each of those was a small daily loss that nobody owned. Finance typed every supplier bill and expense claim into the ERP by hand. Certificates and supporting documents were checked by whoever had time. Enquiries on WhatsApp landed on personal phones with no record that they had existed. Out-of-hours callers reached a ring tone and called the next supplier. None of it justified a new hire, and all of it together was a lot of hours a month.

## My responsibility
I designed all five systems, I built them, and I own them in production. They are my responsibility in the same way the ERP and the network are: monitored, fixed when they break, and switched off if they misbehave.

## Solution
Five systems, each doing one job, all writing into the ERP the group already runs on.

1. Document OCR into the ERP. Supplier bills and expense claims are read by vision-capable models and created as records in Odoo with the original document attached. A person approves each one. The pipeline never posts to the ledger.
2. Automated certificate and document verification. It checks whether a document is what it claims to be and whether its details match what we expect, then flags exceptions for a person. It refuses to guess.
3. A 24 hour AI sales agent on WhatsApp and the group websites. It answers, works out what the enquiry actually is, and creates a qualified lead in the Odoo CRM pipeline. Anything about price or delivery goes to a person.
4. An AI voice agent on our Grandstream telephony. It answers inbound calls on a phone platform inside my own estate rather than a third-party cloud, so caller audio does not leave it.
5. One AI chat platform running several WhatsApp numbers and the websites from a single place, so each brand answers in its own voice from one set of rules, and adding a number is configuration rather than a project.

## Technology
Vision-capable and language model APIs (Gemini and Claude among them), Python, Odoo and its API, PostgreSQL, WhatsApp, Grandstream telephony, Linux and Nginx.

## Implementation
The order was deliberate. OCR first, because a paper trail makes accuracy measurable. Verification second, on the same pipeline pattern. Then the sales agent, the chat platform behind it, and finally voice once chat had proved where the boundaries sit. Each one went live with a review queue, an audit log, idempotency so the same document cannot post twice, and a switch-off rule agreed before go-live.

## Challenges
The model is the least of it. A supplier changes an invoice template and the OCR quietly starts picking a different number, which is why review is not optional. WhatsApp sessions drop, and something running unattended for months has to be built for reconnection rather than for the happy path. An agent that invents an answer is worse than no agent, so deciding what each system must escalate took longer than making it work.

## Result
Finance checks values instead of typing them. Documents are checked every time and leave a record. An enquiry at two in the morning gets a proper answer and arrives in the ERP as a qualified lead. Callers reach something that can act. All five run every day inside a working manufacturing group, owned and monitored like any other production system.

## Verified evidence
All five systems are in production at the group. The OCR, the sales agent and the voice agent each have their own case study on this site with the evidence they rest on. I hold the logs and can produce processing counts, exception rates and after-hours shares on request. I do not quote figures I have not measured.

## Skills demonstrated
Applied AI in production, pipeline and validation design, ERP integration, conversational and voice agent design, telephony, unattended service reliability, AI governance inside a business.

## Suitable target roles
Head of Digital and AI Transformation, IT Director, Head of IT.

## Three interview talking points
1. "Five systems, one rule: they create records for a person to check. None of them posts or pays."
2. "OCR went first because a paper trail makes accuracy measurable. Voice went last because chat had to prove the boundaries first."
3. "The failures were never the model. A changed invoice template, a dropped WhatsApp session, an answer that should have been escalated."
