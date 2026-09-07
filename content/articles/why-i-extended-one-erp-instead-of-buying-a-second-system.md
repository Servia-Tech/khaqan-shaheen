---
title: Why I extended one ERP instead of buying a second system for manufacturing
description: A second manufacturing system means a second set of records and an interface to maintain forever; extending one Odoo instance kept six sites on one set.
date: 2026-09-08
type: article
tags: [erp, odoo, manufacturing]
---

# Why I extended one ERP instead of buying a second system for manufacturing

Because a second system means a second set of records and an interface that somebody maintains forever. I had the manufacturing modules the standard package lacked built on top of the ERP the group already ran, to my specification, and kept them upgradable. Six sites now close the month from the same records.

## What six sites looked like before one platform

The group I run IT for makes plastics at six sites in five countries, with around 150 people using the systems and support coming from Dubai. When I took on the whole function, each site had bought its own software locally over the years. Nothing was shared, there was no standard, and nobody owned the whole.

The cost of that showed up at month end. Production ran on one set of numbers, finance on another, sales on a third. Consolidating the group meant exporting from one system, retyping into a spreadsheet, and then arguing about the differences the retyping had quietly invented. A simple question about the whole group took a week to answer, and the answer depended on who had done the export.

I report directly to the owner with no IT layer above me, so the ERP was mine to decide and mine to deliver. The obvious first step was one ERP for the group. The harder question was what to do about manufacturing.

## Why not just buy a manufacturing system?

Stock ERP software is good at accounting, sales, purchasing and stock. It is weaker on a plastics plant. Ours has machines with different capacities, shifts, batch issue of material, and a path from a customer enquiry through a manufacturing order to a delivery order that the standard package did not model the way we work.

The usual answer is a second product. You keep the ERP for finance and buy a manufacturing system for the plant, then connect the two. Every vendor in the space will tell you the interface is straightforward. It never is, and even when it works on day one it has to work on every day after that, through every upgrade of either side. Somebody owns that interface for the life of both systems, and in a group of our size that somebody is me.

Two systems also means two sets of records. The manufacturing order in one product and the sales order in the other are supposed to agree. When they don't, you are back to the reconciliation exercise you bought the ERP to get rid of. I had just done the work of getting six sites onto one set of numbers. I was not going to split them again at the plant door.

So I chose to extend. One Odoo instance for the group, covering production, sales, inventory, procurement, accounting, HR and maintenance, with the modules the standard package did not reach built on top of it.

## What had to be built

The gaps were specific. Order management from enquiry to delivery. Quotation and pricing that understood our products. Lead capture feeding the same pipeline. An accounting approval flow where a rejected bill carries a recorded reason. Dashboards by function, so a plant manager and a finance manager each see their own view. Barcode and label printing on the shop floor.

I do not write this code myself. I specify it, external developers build it to that specification, and I review what comes back against what I asked for. That division matters. My job is to know the business well enough to write a specification a developer can build without guessing, and to know Odoo well enough to reject a design that will not survive.

Where a good community module already existed for a gap, I deployed and maintained it rather than having it rebuilt. That is a different claim from having written it, and I am careful about which is which. An ERP-literate reader will check.

## Keeping the customisation upgrade-safe

Customisation is what kills ERP platforms. Heavily modified systems become impossible to upgrade, and the group ends up stranded on an unsupported release with a vendor who has moved on. The point of extending one system rather than buying two was to stay on a supported platform, so upgradability was a design constraint on every module from the start, not something to think about later.

In practice that means a few rules I apply to every specification.

- Extend the standard models, never fork them. A custom field on a standard model survives an upgrade. A copied and edited core module does not.
- Keep custom code in its own module tree, with the company as author, so it is obvious what is ours and what is Odoo's.
- Never patch the core to fix a problem. If the framework does not allow something cleanly, the specification changes, not the framework.
- Treat the upgrade as a rehearsed event. The module tree gets migrated forward on a copy of production before anything touches the live instance.

The module tree I hold today documents more than one generation of the platform, each migrated forward from the last. That is the evidence the approach works. If it had not, we would still be on the version we started on.

## How do you get six sites to accept one standard?

The technical work was the easier half. Sites that had chosen their own tools had to be persuaded that a group standard was worth what they were giving up, and a site manager who picked his own tools is not going to enjoy being told they are going.

I rolled out site by site and function by function rather than one switch-over. That gave each site a period where their local system and the group system ran together, which is uncomfortable but honest. It also gave me a rule for every difference that came up. Where a local difference was real, such as a legal requirement in that country or a genuinely different production flow, it went into the configuration. Where it was habit, it was standardised. Most differences turned out to be habit, and saying so plainly at the start saved a lot of argument later.

The other thing that helped was the reporting line. The ERP was mine to decide, and I report directly to the owner, so nobody at a site could appeal over my head for a different answer. I could spend my time explaining how the group standard would work rather than defending whether it should exist.

## What changed at month end

All six sites now run on one supported platform and close the month from the same records. The reconciliation exercise is gone because there is nothing to reconcile. A question about the whole group is a report, not a project. And the manufacturing side of the business lives in the same system as the invoice it produces, so the order that went to the machine and the order that went to the customer are the same order.

It is not a finished job. The tree keeps growing as the group grows, and each new module has to pass the same upgradability test as the first.

## Common questions

### Does extending Odoo mean you are locked into one version?

No, provided the extensions are built to survive upgrades. Ours are kept in their own module tree, extend the standard models rather than forking them, and never patch the core. Each upgrade is rehearsed on a copy of production first, and the platform has been migrated forward more than once since the first build.

### Why not run a separate ERP in each country?

Because the whole problem was six sites closing the month off six sets of records. Local requirements that are real, such as a tax rule or a customer document format, go into the configuration of the one instance. Running separate instances would recreate the reconciliation exercise we removed.

### When would you buy a second system instead?

When the gap is a whole discipline the platform was never designed for and the interface would be simple, such as a machine-level control system that only reports finished quantities. For order management, pricing, approvals and shop-floor printing, which all touch the same records as sales and finance, extending the one platform was the right call.
