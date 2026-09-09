---
title: "Bringing a new factory online: the order of operations"
description: Cabling and circuits first, then security, ERP, identity, telephony and site devices. The sequence that puts a new factory on group systems from opening day.
date: 2026-09-08
modified: 2026-09-10
type: article
tags: [infrastructure, manufacturing, project-delivery]
---

# Bringing a new factory online: the order of operations

Cable while the builders are there, order the circuits first, secure the perimeter, connect the site to the group ERP, then identity, telephony and site devices, then hand over. Each layer depends on the one before it. Done out of order, you do them twice, and the site opens on spreadsheets it never gives up.

## IT is on the critical path whether anyone says so or not

When the group commits to a new factory, the building work has a date and the commercial plan assumes the site can trade from that date. Nobody writes IT into the critical path. It is there anyway. A plant with no systems cannot receive material, book production or raise an invoice, so it cannot trade, however finished the building looks.

The failure mode is well known and expensive. The site opens, the systems are not ready, and it runs on spreadsheets and local workarounds "for a few weeks". Those weeks become months. The workarounds have to be unpicked and reconciled later, and by then the site has its own way of working and does not want to give it up. That is how a group ends up unable to close the month off one set of records.

I own the build: network, servers, connectivity, ERP, identity, telephony and physical security, delivered as one project from Dubai with my team of six and the local vendors I select and contract. The sequence below is the checklist I use each time.

## Cabling and the equipment room, while the builders are still there

Physical and network first. Containment, structured cabling and the equipment room get designed in during construction, because retrofitting cable into a finished factory costs several times more than running it while the walls are open. That means being in the drawings before the fit-out contractor is appointed, and being on the calls where the building programme changes, because it will.

The equipment room is the item most easily forgotten. It needs power, cooling, a lockable door and enough space for the site to grow, and if it is not on the plan it becomes a cupboard next to the compressor.

## Why do the circuits get ordered first?

Because carrier lead times are the longest single item in the whole project and the one I have least control over. Every country has its own carriers, its own customs timelines and its own local contractors, and none of them care about the group's opening date. Equipment can sit in customs for longer than the fit-out takes.

So local circuits are ordered as soon as the site has an address, before the network design is even finished. If the circuit arrives early it waits. If it arrives late the site opens without a connection to the group, and everything that follows waits with it. Connectivity to the group is what makes the site part of the estate rather than an island with a logo on the gate.

## Perimeter and security before anything connects

The site gets a firewall and a site to site VPN to the group standard before a single device is connected to anything. It is much easier to build a site to the standard than to bring it up to the standard afterwards, and a site that has spent weeks open to the internet while waiting for "the security phase" is a site I now have to treat as compromised.

I do not publish the standard. The point is that there is one, it is the same at all six sites, and a new site inherits it on day one rather than earning it later.

## The ERP site record and identity

Servers and ERP connectivity come next, so that the site works in the group's system of record from the first day rather than in a local copy. In practice that means creating the site inside the one Odoo instance: its company record, its warehouses and locations, its local accounting configuration for that country, its sequences and its printing. The site does not get its own ERP. It gets a place in the group's.

Identity runs alongside, as the new team is hired. Each person gets one Google Workspace identity with single sign-on, two factor authentication and role-based groups, the same way every other site works. Because roles already exist, a new site's staff are assigned to roles rather than having access invented for them. A storekeeper at the new site has the same access as a storekeeper at any other.

This is the point where the site can trade. It can receive material, book production and raise an invoice, on the group's records, before the last painter has left.

## Telephony on the group platform

The site goes onto the group telephony platform and is reachable on the group numbering from the start. Telephony sits inside my IT function rather than with facilities, which means it is part of the same project and the same sequence rather than something a local supplier installs later and I inherit. It also means anything built on the group platform, including the AI voice agent that answers calls on our Grandstream telephony, is available to the new site rather than being something to rebuild locally.

## Site devices: biometric readers, IP CCTV, access control, label printers

Last of the technical layers is physical security and the devices on the floor. Each is connected to the system it feeds, which is the point of doing them after the ERP and the network rather than before.

- Biometric attendance readers, feeding attendance into the ERP so a shift is a record rather than a paper sheet.
- IP CCTV, on its own network segment, viewable from the group.
- Access control on the doors that need it, managed as part of the estate rather than as a stand-alone box on the wall.
- Label printers on the shop floor, driven from the ERP so a barcode label comes from the same record as the manufacturing order.

Device and systems integration is where the local contractor and my team meet. The contractor pulls cable and mounts hardware. My team makes each device part of the estate.

## The day one checklist

Before I let a site open on group systems, I want to be able to answer yes to every one of these.

- The circuit is live and the site to site VPN is up.
- The firewall is on the group standard.
- The site exists in the ERP with its warehouses, locations and local accounting in place.
- Every hired person has one identity, a second factor enrolled and a role.
- The site's numbers ring on the group platform.
- Attendance readers, CCTV, access control and label printers are connected and feeding the systems they belong to.
- Local hands are contracted, documentation is done, and the site is inside the normal support arrangement.

That last line is the handover, and it is the one that gets skipped when the opening date is close. A site with no local hands and no documentation is a site that phones Dubai for every printer jam.

The dates always move. The plan has to survive dates changing underneath it, and the sequence is what makes that possible. If the order is right, a slip in one layer delays the next layer, not the whole project.

## Common questions

### What happens if the circuit is not ready on opening day?

The site can still be built and configured to the group standard, but it cannot trade on group systems until it is connected, which is why circuits are ordered before almost anything else. A temporary connection buys time. Anything that lets a site "start on spreadsheets" is avoided, because those spreadsheets are still there a year later.

### Why not let a new site pick its own local systems?

Because that is exactly how the group ended up with six sites on six systems before the ERP consolidation. A new site joins the group's one instance as a company record with its own warehouses and local accounting, so it closes the month from the same records as everyone else from its first month.

### How do you deliver this from Dubai?

With local vendors I select and contract myself for cabling, mounting and hands-on work, and my own team for everything that makes the site part of the estate: the firewall, the VPN, the ERP configuration, identity, telephony and device integration. Vendor selection and negotiation are part of the job, not a procurement handoff.
