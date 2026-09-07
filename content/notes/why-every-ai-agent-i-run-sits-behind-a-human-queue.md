---
title: Why every AI agent I run sits behind a human queue
description: Because a language model is confidently wrong in a way a scanner never is, every agent I run creates records for a person to check and none of them post or pay.
date: 2026-09-08
type: note
tags: [ai-in-production, erp, review-queue, governance]
---

# Why every AI agent I run sits behind a human queue

Because a language model is confidently wrong in a way a broken scanner never is. Every agent I run creates a record, a draft or a lead for a person to check. None of them post a journal entry, pay a supplier or commit the company to a price.

The five systems I have in production all follow the same pattern, and it was a decision rather than an accident. The OCR pipeline creates draft bills. The sales agent creates leads and hands anything commercial to a person. The others draft and suggest. Between each model and anything that has consequences, there is a queue with a human on the other end of it.

The first reason is the failure mode. A scanner that breaks gives you a blank page or an error. A model that breaks gives you a plausible answer in a full sentence, with a reason attached. You cannot catch that with an exception handler, because nothing was thrown. You catch it with a person who knows what a bill from that supplier normally looks like, or what a serious enquiry sounds like. The second reason is cost. Checking a draft takes a person a moment. Unwinding a posted entry across two companies' books, or apologising to a customer for a price the bot invented, takes a morning and a phone call. When review is that much cheaper than the mistake, the queue pays for itself the first time it catches one.

The third reason is that the queue is where trust gets built, and there is no other place to build it. Finance did not trust the OCR on day one and had no reason to. They trust it now because they have checked its output for long enough to know where it fails. Their review notes are the evaluation set I could never have written myself, because I do not know what a wrong bill looks like as well as they do. The fourth reason is that it made the rollout possible at all. Nobody had to approve the sentence "the AI posts to the ledger". They approved "the AI fills in the form and you press the button", which is a much easier sentence to say yes to.

The queue narrows over time, by category, as the notes show a category has been clean for long enough. It will never narrow to zero for anything involving money. If I ever remove the review for some class of document, it will be because months of review notes say nothing happened, not because a model scored higher on a benchmark.
