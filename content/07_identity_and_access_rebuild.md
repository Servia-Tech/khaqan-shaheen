# Identity and access: from local passwords to single sign on with two factor

## Situation
A manufacturing group with around 150 users across six sites in five countries. Each site had bought and set up its own systems locally over the years, so identity had never been designed. It had accumulated.

## Business problem
Passwords were held per system and per site. The same person had separate credentials for the ERP, for mail and for whatever else their site had bought, which guarantees one weak password reused across all of them. There was no central control and no reliable way to answer the basic questions: who has access to what, and who still has access who should not. Leavers were the sharp edge. Removing access meant remembering every system a person had touched, so accounts survived departures. Inside the ERP, everybody could see everything.

## My responsibility
I own the security and identity estate for the group and report to the owner. This rebuild was my proposal, my design and my delivery, across all sites.

## Solution
One identity per person on Google Workspace, with single sign on and OAuth, two factor authentication enforced, and access granted through role-based groups rather than individually.

Access inside the ERP was rebuilt on the same principle. Odoo expresses access as user groups, record rules and per-model access lists, so I defined those properly: a salesperson sees the records their role allows and nothing else.

Joiners and leavers became a role change instead of a search. Somebody leaves and access is withdrawn the same day, in one place, rather than site by site from memory. On top sits login and activity monitoring with automated alerts, so unusual access is visible as it happens rather than discovered afterwards.

## Technology
Google Workspace administration, single sign on, OAuth, two factor authentication, role-based access control, Odoo security groups and record rules, logging and monitoring tooling.

## Implementation
Identity first, then the application layer, then monitoring. Two factor was introduced with the enrolment support a factory workforce actually needs, not as an announcement. Roles were defined with the managers who own the data, because a role model nobody agreed to gets bypassed within a month.

## Challenges
Two factor across a manufacturing workforce is a practical problem before it is a technical one. Not everybody sits at a desk or has a company handset, and shop-floor patterns are not office patterns. Tightening access also always takes something away from somebody, so every restriction needs a person who will defend it. I could do that because the mandate came from the owner.

## Result
One identity per person, with a second factor. Access follows the role and is withdrawn on the day someone leaves rather than whenever it is noticed. Unusual access raises an alert instead of surfacing later.

## Verified evidence
Access control inside the ERP is defined in the custom module tree I hold, as user security groups, record rules and per-model access lists. The identity layer is the group's live Google Workspace tenant, which I administer. I publish no policy detail, no role model, no monitoring rules and no tenant detail, because that is the part an attacker would want.

## Skills demonstrated
Identity and access management, Google Workspace administration, single sign on, OAuth and two factor authentication, role-based access control, security monitoring.

## Suitable target roles
IT Director, Head of IT, IT Governance and Security leadership.

## Three interview talking points
1. "Identity is Google Workspace: single sign on, OAuth, two factor, role-based groups. Leavers are removed the same day, in one place."
2. "Roles are defined in the ERP as groups and record rules and mirrored in the identity layer, so access follows the role rather than a request."
3. "Two factor across a factory workforce is a people problem before it is a technical one. Enrolment support is the project. The configuration takes an afternoon."
