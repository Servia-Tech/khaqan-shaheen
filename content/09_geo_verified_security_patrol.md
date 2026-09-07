# Geo-verified security patrol, integrated with the ERP

## Situation
A manufacturing group with production and storage sites in five countries. Physical security sits inside my IT function alongside IP CCTV and access control, because in a manufacturing group those are IT systems.

## Business problem
Guard patrols were recorded as signatures on paper: a sheet on a clipboard, a time written next to a checkpoint, a signature at the end of the round. The problem is not that guards are dishonest. It is that the record is unverifiable in principle, because a sheet completed in a gatehouse at the end of a shift looks exactly like a sheet completed on the round. Nobody could show that a patrol had happened, so the control existed on paper and not in fact.

## My responsibility
I proposed it, designed it and built it, and I own the physical security estate it belongs to.

## Solution
A patrol application on a phone, where reaching a checkpoint is confirmed by location rather than by a signature, and the record goes straight into the ERP.

The guard walks the round and records the checkpoint on the handset. The system verifies the checkpoint by location at the moment it is recorded, so the evidence is produced by the act itself rather than written down afterwards. The record then reaches management reporting the same way every other operational number does.

I scoped it deliberately narrowly. The system verifies that a checkpoint was reached, which is the control the business actually needs. It is a patrol evidence system, not a tracking system aimed at individuals, and that is a distinction I would defend in any jurisdiction.

## Technology
Android application development and packaging, device location services, Odoo, PostgreSQL, the group's mobile and PWA delivery stack.

## Implementation
Built on the same mobile delivery approach as the group's other field applications, so it is packaged, distributed and integrated the same way. Introduced site by site, with the paper round kept running until the electronic record had proved itself.

## Challenges
Location on a manufacturing site is not the clean signal it is in open ground. Steel-framed buildings, warehouses and plant rooms are exactly where accuracy degrades, and exactly where the checkpoints are. Designing for that, rather than assuming a perfect fix, is most of the engineering. Connectivity is the second problem: a patrol at the far end of a yard at three in the morning cannot depend on a live link. The third is adoption. A system introduced as a way of catching guards out gets defeated within a week. Introduced as the thing that proves they did their job, it gets used.

## Result
Patrol evidence is verifiable rather than assumed, and it reaches management reporting directly instead of as collected paper.

## Verified evidence
Android delivery is verified by build artefacts I hold, including a packaged field tracking application build alongside the group's ERP client. The system runs in production at the group. I do not publish the application build, checkpoint locations, patrol timings or coverage detail, for reasons that are obvious in a security system.

## Skills demonstrated
Android application delivery, location-based system design, ERP integration, physical security operations, designing controls people will actually use.

## Suitable target roles
IT Director in manufacturing, Head of IT, Digital Transformation Manager.

## Three interview talking points
1. "Guard patrols used to be a signature on a clipboard. Now the checkpoint is verified by location from a phone and the record lands in the ERP."
2. "The signature was never the control. A sheet filled in at the gatehouse looks identical to one filled in on the round, so what we had was the appearance of a control."
3. "It verifies checkpoints, not people. Scoped the other way it would have been defeated in a week, and I would not want to defend it."
