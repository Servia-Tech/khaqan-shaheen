# One ERP across six sites in five countries

## Situation
A manufacturing group with six sites in five countries and around 150 users, supported from Dubai. Each site had bought its own software locally over the years. No shared platform, no shared standard, no single owner.

## Business problem
Six sites were not closing the month off the same records. Production ran on one set of numbers, finance on another, sales on a third. Consolidating meant exporting from one system and retyping into a spreadsheet, which is slow and quietly invents differences that then get argued about. No question about the whole group could be answered without a week of work.

## My responsibility
I own the entire IT function and report directly to the owner, with no IT layer above me. I lead a team of six and buy in outsourced development when the pipeline needs it. The ERP was mine to decide and mine to deliver.

## Solution
One Odoo instance for the group, covering production, sales, inventory, procurement, accounting, human resources and maintenance.

The decision that mattered was to extend rather than replace. Stock manufacturing software did not model our plant: machines, capacity, shifts, batch issue, and the path from enquiry to manufacturing order to delivery order. The usual answer is to buy a second system for manufacturing and then maintain the interface between the two forever. Instead I had the modules the standard package did not reach built on top of it, to my specification, so there is one platform and one set of records. That covers order management, quotation and pricing, lead capture, accounting approvals, dashboards by function, and barcode and label printing. Where a good community module already existed I deployed and maintained it rather than rewriting it, which is a different claim from authoring it.

## Technology
Odoo, Python, the Odoo ORM, XML and QWeb, JavaScript, PostgreSQL, Ubuntu Linux, Nginx, with workloads on-premise and across AWS, Google Cloud and DigitalOcean.

## Implementation
Site by site and function by function rather than one switch-over. Where a local difference was real it went into the configuration; where it was habit, it was standardised.

## Challenges
Customisation is what kills ERP platforms. Heavily modified systems become impossible to upgrade and the group is stranded on an unsupported release, so keeping the extensions upgradable was a constant design constraint. The other challenge was people. Sites that had chosen their own tools had to be persuaded that a group standard was worth what they gave up.

## Result
All sites run on a single supported platform and close the month from the same records, instead of six systems and a reconciliation exercise.

## Verified evidence
A custom Odoo module tree I hold and maintain: 28 module directories, 25 carrying the company as author, four being third-party or community modules I maintain rather than claim. The largest module alone holds 22 model files, more than 30 views and eight wizards, with its own JavaScript and QWeb assets. That snapshot documents an earlier generation of the platform, migrated forward since. The code is my employer's and is not published.

## Skills demonstrated
ERP implementation and ownership, multi-country rollout, build-versus-buy judgement, custom module engineering, upgrade-safe architecture, team leadership, vendor management.

## Suitable target roles
IT Director, Head of IT, ERP Manager, Head of Digital and AI Transformation.

## Three interview talking points
1. "One instance, six sites, five countries, around 150 users. I implemented it and I own and direct its development. That is why every site closes the month off the same records."
2. "The easy answer was a second system for manufacturing and an interface to maintain forever. I extended the one we had, and built the extensions to survive upgrades."
3. "Some of what runs there is community code we maintain rather than code built to our specification. I am careful about which is which, because an ERP-literate interviewer will check."
