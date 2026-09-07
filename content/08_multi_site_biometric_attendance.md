# Multi-site biometric attendance, integrated with the ERP

## Situation
A manufacturing group with six sites in five countries and around 150 staff, most of them working shifts in production rather than at desks. Attendance drives payroll, and in a shift operation it also drives production planning.

## Business problem
Attendance was captured locally and then retyped into payroll. Every site had its own way of recording who turned up, and at the end of the period somebody turned that into a payroll input by hand. Retyping is slow and error-prone, and payroll errors are the kind staff notice and remember. Management reporting lagged the month, and there was no group view.

## My responsibility
I designed and delivered the system and I lead the team that runs it. As with everything in this function, I both specify it and build it.

## Solution
Biometric attendance capture at each site, connected directly to the ERP, with the record reaching payroll and management reporting without anyone retyping it. This is device and systems integration: biometric readers at the sites feeding the system of record that already holds employees, contracts and payroll.

Alongside the fixed readers, staff and supervisors reach the system from a phone. I built and packaged an Android client for the group's ERP and made the ERP backend responsive. That mobile layer is the same system rather than a separate app with its own data, which is what keeps the numbers consistent.

## Technology
Biometric attendance devices, Odoo, PostgreSQL, Android application packaging, progressive web application delivery, Linux, site networking across five countries.

## Implementation
One site first, proved against a payroll period run in parallel with the old method, then extended. Running both methods for a period is unglamorous and it is the only way anybody trusts a new payroll input.

## Challenges
Five countries means five sets of local employment practice, and shift and overtime rules are not the same in each. Modelling that without forking the system into five variants took more thought than the device integration did. Sites also lose connectivity, and an attendance system that fails when the link drops is worse than a paper register.

The most important constraint is not technical. Biometric data is sensitive personal data in every jurisdiction the group operates in and in every country I would work in next. The system exists to produce an attendance record, and I do not discuss or publish anything about how biometric data is handled or stored.

## Result
Attendance reaches payroll and management reporting from the record itself rather than from a spreadsheet somebody typed, and a group-wide attendance position exists.

## Verified evidence
Android delivery is verified by build artefacts I hold: packaged application builds for the group's ERP client and a field tracking application, plus signed releases from my own venture. The attendance estate exists as a live system with its own database in my care. I have separately specified and published an attendance register module commercially, which is the same problem solved in public. I publish nothing about biometric data handling and I do not distribute the employer's application builds.

## Skills demonstrated
Device and systems integration, ERP and payroll integration, Android and PWA delivery, multi-country process modelling, handling of sensitive personal data, site networking.

## Suitable target roles
IT Director in manufacturing, Head of IT, Digital Transformation Manager.

## Three interview talking points
1. "Biometric attendance across sites, integrated with the ERP, so payroll works from the record rather than a spreadsheet."
2. "The variation between countries was harder than the hardware. Five sets of local practice, one system, and no forking it into five versions."
3. "Biometric data is sensitive personal data. I will talk about the workflow and the integration, and not about how the biometric data itself is handled. That answer is the same in an interview as it is in public."
