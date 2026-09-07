---
title: "Five AI systems in production: what breaks when nobody is watching"
description: Connections drop, inputs drift and confident wrong answers get through. Running five AI systems in daily production taught me the rules that keep them safe.
date: 2026-09-08
type: article
tags: [ai, production-systems, erp]
---

# Five AI systems in production: what breaks when nobody is watching

Five AI systems of my design run in daily production at the group. What breaks when nobody is watching is rarely the model. It is a dropped connection, a confident wrong answer, or a boundary nobody defined. The fix is the same for all five: a person at the edge, a review queue, and an off switch.

## Document OCR into the ERP

The first system reads supplier bills and expense claims and creates the record in the ERP. A bill or a photographed receipt arrives, the pipeline extracts the fields that matter, and a bill or expense record appears in Odoo with those values populated and the original document attached. It runs on Gemini and Claude vision APIs, with Python between them and the ERP.

The principle from the first version is that the pipeline creates records but never posts to the ledger. A language model is confidently wrong in a way a broken scanner never is. It gives you a plausible total from the wrong line, formatted perfectly. So the output lands in the bill and expense models where the group's existing approval workflow already applies, and finance changed from typing values to checking them.

What breaks unattended: a supplier changes its invoice template without telling anyone, and the field that was reliably in the top right is now somewhere else. The system does not crash. It quietly starts picking a different number. That is why the review step is not optional.

## Certificate and document verification

The second system checks certificates and documents automatically: whether the document is what it claims to be, whether the details on it match what we expect, and whether anything is missing.

It makes no decisions. It raises a flag for a person and shows them why. The failure mode I designed against is the confident pass: a document that looks right, reads right and is wrong in one detail that matters. A system that only ever says yes is worse than no system, because people stop looking. So it is built to refuse to guess and to escalate on doubt, and the person who reviews the exceptions is the same person who would have checked the document by hand before.

## The sales agent on WhatsApp and the web

The third system answers enquiries on WhatsApp and on the group websites at any hour, qualifies the enquiry and creates the lead in the Odoo CRM pipeline. In this market WhatsApp is the first channel a buyer reaches for, and enquiries do not arrive during office hours. They arrive when the buyer is thinking about the problem, often late at night or at a weekend.

The agent's job stops at qualification. It answers the question, works out what the enquiry actually is, and hands over a qualified lead. Anything that binds the company commercially, such as a price or a delivery promise, goes to a person. Deciding what it must escalate was more of the work than making it talk, because a manufacturing buyer asking about a specification will not accept a brochure paragraph, and an agent that invents an answer is worse than no agent at all.

What breaks unattended: the WhatsApp connection. Sessions drop. Something running for months without a person watching has to be engineered for reconnection rather than for the happy path. An agent that is silently down looks, from the outside, exactly like a business that does not answer.

## The voice agent on the phone system

The fourth system answers inbound calls on our Grandstream telephony. Chat had already been solved. Voice is where people still go when the enquiry is urgent, and a caller who reaches a ring tone does not leave a voicemail. They call the next supplier, and there is no record the call ever happened.

Because telephony sits inside my IT function rather than with facilities or an outside supplier, I could build the agent onto our own platform instead of pointing our numbers at somebody else's cloud. Call handling stays inside the estate, caller audio does not leave it, and the design stays under my control.

Voice is far less forgiving than chat. A pause of a second that nobody notices when typing is an awkward silence on a call, so latency was a design constraint from the start rather than a tuning exercise at the end. Callers to a manufacturer in this region speak with a wide range of accents, in several languages, often on a poor line.

What breaks unattended: handover. An agent that traps a caller in a loop is worse than the ring tone it replaced. The fallback behaviour, what happens when it cannot understand or cannot help, was defined before it went anywhere near a live number.

## One chat platform under several numbers

The fifth system is the one people do not see. Rather than a separate bot per brand and per WhatsApp number, one platform drives several numbers and all the group websites, with one set of rules and one place to change them. Each brand answers in its own voice, but there is one system behind it. Adding a number is a configuration change rather than a project.

This is the system that makes the other chat systems operable. When a rule changes, it changes once. When the reconnection logic is fixed, it is fixed for every number.

## What actually breaks?

Looking across all five, the failures fall into a short list.

- Connections drop. WhatsApp sessions, API endpoints, the telephony link. The model is fine and the system is unreachable.
- Inputs drift. A supplier changes a template, callers start arriving in a language last month's calls did not include, a website form gains a field.
- Confidence outruns accuracy. The model produces a clean, well-formatted answer that is wrong, and nothing in the output signals doubt.
- The boundary is crossed. The agent is asked something it should escalate and does not, because nobody wrote that case down.
- Silence looks like success. A system that stops working and stops reporting is indistinguishable from one that is quiet because nothing came in.

None of these is a model problem. They are operations problems.

## The rules I apply to all five

Every system creates or flags, and a person decides. OCR creates a record for finance to approve. Verification raises an exception for a person to clear. The sales agent creates a lead for a salesperson. The voice agent hands over. Nothing posts, commits or promises on its own.

Each has a written boundary: what it answers, what it refuses, what it escalates, and to whom. That document exists before the system goes live, and it changes whenever a real conversation shows it was wrong.

All five are monitored for absence as well as errors. Automated alerts fire when a channel goes quiet for longer than it should, not only when something throws an exception.

Each has a review queue that somebody actually owns. A queue nobody reads is a queue where mistakes accumulate.

And each has an off switch I can reach without a developer. When the voice agent misbehaves, calls go back to the routing they had before it. When the sales agent misbehaves, the number goes back to a person. Knowing you can turn it off in a minute is what makes it safe to leave it on overnight.

## Common questions

### Why let AI create ERP records at all if a person still has to check them?

Because checking is faster and less error-prone than typing, and the document is processed on arrival rather than when somebody is free. The person's job changes from transcription to review, which is where their judgement is actually useful.

### How do you decide what an AI sales agent is allowed to say?

By writing down the boundary before the agent goes live and revising it from real conversations. It answers questions and qualifies the enquiry. Anything that binds the company commercially, such as a price or a delivery promise, goes to a person. When a conversation shows the boundary was in the wrong place, the boundary moves.

### When do you switch one of them off?

When it is doing harm that the review queue cannot catch in time: a voice agent looping callers, a chat agent answering off-script, an OCR pipeline suddenly misreading a common supplier. Each system has a fallback that a person can reach without a developer, and the fallback is always the manual process that existed before.
