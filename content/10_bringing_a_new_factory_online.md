# Bringing a new factory online: the order of operations

## Situation
A manufacturing group that opens new sites. When the group commits to a new factory the building work has a date, and the commercial plan assumes the site can trade from that date. IT is on the critical path whether or not anybody has said so.

## Business problem
A new plant with no systems cannot trade. It cannot receive material, book production or raise an invoice. The failure mode is well known and expensive: the site opens, the systems are not ready, so it runs on spreadsheets and local workarounds "for a few weeks". Those workarounds then have to be unpicked and reconciled months later, by which point the site has its own way of working and does not want to give it up.

## My responsibility
I own the build: network, servers, connectivity, ERP, identity, telephony and physical security, delivered as one project, from Dubai, with my team of six and the local vendors I select and contract.

## Solution
A defined order of operations, because the sequence is the method. Each layer depends on the one before it, and doing them out of order means doing them twice.

1. Physical and network first, while the builders are still on site. Containment, cabling and the equipment room get designed in during construction, because retrofitting cable into a finished factory costs several times more.
2. Connectivity to the group. Local circuits ordered early, because carrier lead times are the longest single item.
3. Perimeter and network security to the group standard, before anything is connected.
4. Servers and ERP connectivity, so the site works in the group system of record on day one rather than in a local copy.
5. Identity. Accounts, single sign on, two factor and role-based groups as the new team is hired.
6. Telephony on the group platform, with the site reachable on the group numbering.
7. Physical security and site devices: IP CCTV, access control, biometric attendance readers and label printers, each connected to the system it feeds.
8. Support handover. Local hands contracted, documentation done, the site inside the normal support arrangement.

## A practical opening-day acceptance checklist

This is a reusable planning template, not a claim that every site has identical requirements. Assign an owner, record the test date and keep evidence for each gate before approving the opening.

| Gate | Demonstration to run | Evidence to retain |
| --- | --- | --- |
| Connectivity | Disconnect the primary circuit during an agreed test window and check the fallback | Outage duration, affected applications and recovery steps |
| Identity | Sign in as a new operator, supervisor and leaver test account | Correct access for active roles; revoked access for the leaver |
| Receiving | Receive a test delivery with the site's actual scanner and printer | ERP receipt, readable label and correct warehouse location |
| Production | Release a representative order to the intended machine | Materials, machine reservation and operator permissions checked |
| Dispatch | Complete a test pick, pack and dispatch with the business owner | Stock movement and document chain reconciled |
| Recovery | Restore a recent backup into an isolated test environment | Restore duration and application-level verification |
| Support | Raise a test incident through the agreed support channel | Named owner, escalation route and local contact |

Download the [factory readiness worksheet](../assets/downloads/factory-it-readiness-checklist.csv). Record **Not tested**, **Pass** or **Needs action** rather than converting an unknown into a green status. Agree acceptable interruption and recovery limits with the business before testing.

For the scheduling gate, see the [Odoo overlap-prevention tutorial](../tutorials/odoo-stop-two-work-orders-booking-the-same-machine.html). For a scoped review before opening, see [ERP consulting in Dubai](../odoo-erp-consultant-dubai.html).

## Technology
Structured cabling and site networking, firewalls and site to site VPNs, Linux servers, ERP and database connectivity, Google Workspace identity, Avaya and Grandstream telephony, IP CCTV and access control.

## Implementation
Delivered remotely from Dubai with local vendors, whose selection and negotiation are part of the same job for me, not a procurement handoff.

## Challenges
Every country has its own carriers, its own customs timelines and its own local contractors, and none of them care about the group's opening date. Equipment can sit in customs for longer than the fit-out takes, and building programmes move late, so the plan has to survive dates changing underneath it.

## Result
A new site trades on group systems from opening day, so there is no reconciliation project afterwards.

## Verified evidence
This is a repeated delivery rather than a code artefact, and the evidence is the estate itself: six sites in five countries on one ERP instance, one network standard, one identity platform and one security standard. The sequence above is my own checklist, published without site names or dates.

## Skills demonstrated
Greenfield IT delivery, project sequencing, multi-country vendor and contract management, network and infrastructure design, budget ownership.

## Suitable target roles
IT Director, Head of IT, especially in expanding or acquisitive groups.

## Three interview talking points
1. "When the group opens a factory, I build the IT: network, servers, ERP connectivity, telephony and security. The site trades on group systems from opening day."
2. "The order is the method. Cable while the builders are there, order the circuits first, and get the site onto the group system of record on day one."
3. "The commonest failure is letting a new site run on spreadsheets for a few weeks. That is how a group ends up unable to close the month off one set of records."
