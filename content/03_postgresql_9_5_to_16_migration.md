# PostgreSQL 9.5 to 16: eight major versions, no unplanned downtime

## Situation
The production database under a group ERP serving six sites in five countries. Everything the group does commercially lives in it. If it stops, six sites stop.

## Business problem
The database was eight major versions behind, on PostgreSQL 9.5. That is a support problem and a security problem at once: security fixes had stopped arriving, and newer tooling assumed a database far ahead of ours. The reason it had been left alone is the usual one. It was the most business-critical thing in the company and nobody wanted to be the person who touched it. There was also no dependable recovery position, so nothing answered the question a manufacturer needs answered: if this server dies on a Tuesday morning, what happens.

## My responsibility
Mine alone, as owner of the platform. I planned the upgrade, rehearsed it, executed it across every site and built the recovery estate around it. There was nobody above me in IT to sign it off, so the risk assessment and the rollback decision were mine too.

## Solution
I took the database from 9.5 to 16, eight major versions, with no unplanned downtime at any site.

The work was not the upgrade. The work was everything around it. I rehearsed the migration on a copy of production and ran the application against the result, because a heavily customised ERP is where major-version behaviour changes bite: query plans move, deprecated behaviour disappears, and every extension has to exist on the new version before you find out live that one does not. Each step had a rollback position I could reach inside the planned window, and sites moved one at a time.

Around the database I built the resilience layer that had not existed: automated backups, point in time recovery, off-site and NAS replication, and monitoring with automated alerts. Recovery stopped being a question about the last backup and became a question about a chosen moment.

## Technology
PostgreSQL, Ubuntu Linux, Nginx, replication and backup tooling, monitoring, Odoo as the application above it.

## Implementation
Rehearse, verify the application, plan the rollback, take a planned window, move, verify again, and keep the old position available until the new one had proved itself. Repeated per site. Deliberately unexciting.

## Challenges
The exposure is asymmetric. A good upgrade is invisible; a bad one is the worst day the company has had. Customisation makes it harder, because the tests that matter are the group's own workflows rather than generic benchmarks. So do time zones: a window that is comfortable in one country is the middle of a working day in another.

## Result
The production database is current and supported. No site suffered unplanned downtime. A failed server is now a documented restore rather than an incident with an unknown outcome.

## Verified evidence
This work leaves an operational record rather than a code artefact. The estate for six sites runs on the current major version, and the backup, replication and monitoring estate runs daily. I hold the change and maintenance records and can produce the window detail in an interview. I do not publish backup locations, retention windows or the recovery runbook.

## Skills demonstrated
PostgreSQL administration and major-version migration, business continuity and disaster recovery design, risk assessment and rollback planning, Linux administration, change management across time zones.

## Suitable target roles
IT Director, Head of IT, Head of Technology, IT Infrastructure Manager.

## Three interview talking points
1. "Nine point five to sixteen, eight major versions, on the live ERP for six sites. Planned windows, no unplanned downtime anywhere."
2. "The rehearsal and the rollback plan were the work. If I cannot get back inside the window, I am not starting."
3. "I rebuilt backup and recovery from nothing at the same time, so a failed server became a documented restore."
