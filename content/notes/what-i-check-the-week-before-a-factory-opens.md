---
title: What I check the week before a factory opens
description: Two links with a tested failover, the company and warehouse in the ERP with local tax and numbering, printers on the floor, users logged in once, and a restore.
date: 2026-09-08
modified: 2026-09-10
type: note
tags: [erp, infrastructure, new-site, checklist]
---

# What I check the week before a factory opens

Two internet links with a failover I have tested by pulling the cable, the new company and warehouse in the ERP with local tax and numbering, printers and scanners on the floor, every user logged in once, and a backup I have restored from. The list is short because the failures are boring.

## Connectivity first

Connectivity first, because the ERP is central and a site with no link has no delivery notes, labels or stock moves. Two links from different providers, and the failover proved by unplugging the primary and watching, not by reading the configuration. The tunnel to the group comes up on both. I have been shown a configured failover and then watched it not fail over, so I no longer take anyone's word for it.

Then the ERP. The company record, its currency and fiscal year. The tax configuration for that country, different every time and the thing most likely to make the first invoice wrong. The warehouse, its locations and routes. The numbering sequences for invoices, delivery notes and purchase orders, per company, because a sequence left on the default will number the new site's documents into another company's range. I have had numbering wrong on day one and spent the first week fixing documents that had already gone out. Units of measure, the shared product master, and the intercompany rules that let the new site buy from the others.

## The ERP and the factory floor

Then the floor, which is where opening day goes wrong. Label printers on the network with the right driver on the right machine. Barcode scanners paired and tested on a real product. The PC at the packing station and at the weighbridge, if there is one. The shared office printer nobody thought was IT's problem until the first invoice needed printing. What stops a line on the first morning is almost never a server. It is a printer.

Then people. Accounts created, roles assigned, and every person logged in once from the machine they will use, so day one is not password day. One named person on site who can restart the router and the print server and knows who to call. Training happened weeks earlier; this is the check that it took.

## People, recovery and the overlooked details

Then the backup. The new site's data is in it, and I have restored one record from it. Time zone on every server, or a factory in a different zone posts stock moves with the wrong date. And the item I always underestimate, the one nobody owns: the cabinet the switch sits in, its power, and the cooling. It is not IT until it fails, and then it is nothing but IT.
