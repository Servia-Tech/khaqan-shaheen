---
title: A PostgreSQL upgrade nobody was allowed to notice
description: Rehearse on a copy of production, keep a rollback inside the window, move one site at a time. PostgreSQL 9.5 to 16 with no unplanned downtime at any site.
date: 2026-09-08
type: article
tags: [postgresql, database, business-continuity]
---

# A PostgreSQL upgrade nobody was allowed to notice

I took the production database under our group ERP from PostgreSQL 9.5 to 16, eight major versions, with no unplanned downtime at any site. The upgrade itself was the small part. The rehearsal, the rollback plan and the backup and recovery estate built around it were the work.

## Why was it left so long?

The database under the ERP holds everything the group does commercially: every order, every stock movement, every invoice, for six sites in five countries. If it stops, six sites stop. That is exactly why nobody had touched it. It was the most business-critical thing in the company, and the person who upgrades it and breaks it is the person everybody remembers. So it sat on 9.5 while the versions went past.

The reasons to leave it alone are all short-term and the reasons to move are all long-term, which is how a database gets eight versions behind without anyone ever deciding that it should. Security fixes had stopped arriving for 9.5. Newer tooling, including the backup and monitoring tools I wanted, assumed a database far ahead of ours. Each year of waiting made the eventual jump larger and the excuse for not making it stronger.

There was a second problem that worried me more than the version number. There was no dependable recovery position. If the server had died on a Tuesday morning, nobody could have said with confidence what the group would get back or when. A manufacturer needs that question answered, and it was not.

I own the platform and report to the owner, with no IT layer above me. That meant nobody was going to sign this off for me. The risk assessment and the rollback decision were mine, which concentrates the mind.

## What was actually at risk

The risk in a major-version upgrade sits above the database, not inside it. A heavily customised ERP is exactly where major-version behaviour changes bite. Query plans move, so a report that ran comfortably on 9.5 can crawl on a newer planner. Deprecated behaviour that the old version tolerated is simply gone. Every extension the database uses has to exist and behave on the new version, and you would rather find out that one does not on a copy than in production with six sites waiting.

The exposure is asymmetric. A good upgrade is invisible. A bad one is the worst day the company has had. So the tests that matter are not generic database benchmarks. They are the group's own workflows: raise a manufacturing order, receive stock, post an invoice, close a period, print a label. If those work on the new version, the upgrade works. If one of them does not, nothing else matters.

## Rehearsing on a copy of production

The rehearsal was the centre of the plan. I restored a copy of production, ran the migration against it, and then ran the ERP against the result. Not a smoke test. The actual application, the actual custom modules, the actual reports the finance team runs at month end.

That surfaced the things a checklist never would have. Behaviour that was silently tolerated on the old version and rejected on the new one. Custom queries whose plans changed. Extension versions that had to be lined up before the move rather than after. Each of those was fixed on the copy and the migration was run again from the start, until a full rehearsal went through cleanly with the application working on the other side.

I kept repeating rehearsals until the run was boring. Boring was the goal. An upgrade that surprises you in rehearsal is doing its job. An upgrade that surprises you in production has already failed.

## The rollback rule

Every step had a rollback position I could reach inside the planned window. That was the one rule I would not bend. If I cannot get back to where I started before the window closes, I am not starting.

In practice that meant keeping the old position intact and available until the new one had proved itself under a real working day, rather than declaring victory the moment the migration finished. A rollback you have to improvise at three in the morning is not a rollback. It is a second incident.

## Moving one site at a time across time zones

Six sites in five countries do not share a quiet hour. A window that is comfortable in one country is the middle of a working day in another. So sites moved one at a time, each in a planned window agreed with that site, with the rest of the group told what was happening and when.

The sequence per site was deliberately unexciting. Rehearse. Verify the application on the copy. Plan the rollback. Take the planned window. Move. Verify again on the live system. Keep the old position available until the new one has earned trust. Then the next site, until every site was on the current version.

Nobody noticed, which was the brief.

## What the backup and recovery estate looks like now

The upgrade was the excuse to build the resilience layer that had never existed. Around the database there are now automated backups, point in time recovery, replication off-site and to NAS storage, and monitoring with automated alerts. It runs on Linux with Nginx in front of the application, with workloads on-premise and across AWS, Google Cloud and DigitalOcean.

The change that matters is the question recovery answers. Before, it was a question about the last backup: when was it taken, did it complete, has anyone ever restored from it. Now it is a question about a chosen moment. A failed server is a documented restore to a point in time, not an incident with an unknown outcome.

I do not publish backup locations, retention windows or the recovery runbook, and I would not trust anyone who did. But the estate runs daily, it is monitored, and a restore is a documented procedure rather than an assumption.

## What I would do differently

Two things.

First, I would build the backup and recovery estate before the upgrade rather than alongside it. I did both in the same programme because both were overdue, but the honest order is recovery first. A rehearsed restore is the safety net under everything else, and I would rather have had it in place before I started moving versions.

Second, I would never again let a database get eight versions behind. The safest upgrade is a small one, done regularly, on a system where upgrading is a normal event rather than a feared one. The whole programme existed because that habit had not. It exists now. The database is current and supported, and the next major version will be one step, rehearsed the same way, in a window nobody notices.

## Common questions

### How do you test an ERP against a new database version?

By restoring a copy of production, migrating it, and running the real application against the result: the custom modules, the month-end reports, the shop-floor printing. Generic database benchmarks tell you nothing about whether your own workflows will survive. The rehearsal is repeated until it runs cleanly end to end.

### What does point in time recovery actually give you?

The ability to restore the database to a chosen moment rather than to the last completed backup. If somebody deletes the wrong records at ten past nine, you can recover to nine o'clock. It turns a failed server or a bad change from an incident with an unknown outcome into a documented restore.

### Is it safer to upgrade in small steps every year?

Yes. The cost of a major-version upgrade grows with the gap, and so does the fear of doing it. A database that moves one version at a time, rehearsed each time, carries far less risk than one that waits eight versions and then has to move all at once.
