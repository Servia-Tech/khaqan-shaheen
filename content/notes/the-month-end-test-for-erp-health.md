---
title: The month-end test for ERP health
description: If six sites can close the month from the same ERP records without a spreadsheet, the ERP is healthy; a spreadsheet at month end means a record is missing.
date: 2026-09-08
modified: 2026-09-10
type: note
tags: [erp, odoo, month-end, finance]
---

# The month-end test for ERP health

If every site can close the month from the same records without opening a spreadsheet, the ERP is healthy. If a spreadsheet appears, something the business needs is not in the system. Everything else on the dashboard is detail.

## What close reveals

I run one ERP across six sites in five countries. Different tax regimes, different currencies, different public holidays, one database. For most of the month those differences do not have to agree with each other. At month end they do. Close is the only moment when every site's stock, sales, purchases and payroll are tested against the bank statement and the tax return at the same time, and it is the only test of the system that is not a proxy for something else.

The spreadsheet is the symptom I watch for. Somebody reconciles stock in Excel because the valuation report does not match what they counted. Somebody recalculates landed cost by hand because the freight invoice arrived after the receipt was posted. Somebody keeps a list of intercompany invoices because the two companies' records do not tie. Each of those is a missing record, a missing report, or a process that lives in one person's head instead of in the system. The spreadsheet is not the problem. It is the bug report.

## Read the spreadsheet as a bug report

So I do not ask whether the ERP is up. It is up, and uptime is the entry fee, not a result. I ask each site's accountant what else they had open during close. Then I go and find the record that spreadsheet is standing in for. Sometimes it is a report that was never built. Sometimes it is a workflow the site has been doing on paper since before the migration. Sometimes it is a configuration error, a fiscal position or a cost method set wrong on one company, that has been quietly producing numbers people learnt to correct by hand.

There have been closes where the spreadsheet was the honest answer, and I would rather know that than have it hidden. The fix has always been a report or a workflow. It has never been a memo telling people to stop using Excel, because people use Excel when the system has let them down, and telling them off does not repair the system.

## Fix the missing workflow

Ticket counts, dashboards and satisfaction surveys all measure something. Month end measures whether the records are true. A spreadsheet at close is a bug report, and I read it like one.
