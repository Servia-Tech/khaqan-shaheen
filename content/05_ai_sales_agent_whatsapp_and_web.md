# A 24 hour AI sales agent on WhatsApp and the group websites

## Situation
A manufacturing group selling into several countries, with four brands, four websites and several WhatsApp business numbers. In this market WhatsApp is the first channel a buyer reaches for, ahead of email and ahead of the phone.

## Business problem
Enquiries do not arrive during office hours. They arrive when the buyer is thinking about the problem, often late at night or at a weekend, and one that waits until Sunday morning has usually been answered by somebody else first. Enquiries also landed in personal inboxes and on individual phones, so there was no reliable record they had existed. Nobody could say how many the group received, let alone how many were lost.

## My responsibility
I designed and built it and I own it. It is one of five AI systems of my design running in daily production at the group.

## Solution
A conversational agent that answers enquiries on WhatsApp and on the group websites, at any hour, then qualifies the enquiry and creates the lead in the ERP.

The architecture matters more than the chat. Rather than a separate bot per brand and per number, I built one platform driving several WhatsApp numbers and the websites, with one set of rules and one place to change them. Each brand answers in its own voice, but there is one system behind it, which is why adding a number is a configuration change rather than a project.

The agent's job stops at qualification. It answers the question, works out what the enquiry actually is, and creates a qualified lead in the ERP pipeline. Anything that binds the company commercially goes to a person.

## Technology
Large language model APIs, WhatsApp, Python, Odoo CRM, web integration, PostgreSQL.

## Implementation
Wired into the ERP lead pipeline that already existed, so leads land where the sales team already lives.

## Challenges
An agent that invents an answer is worse than no agent at all, so the boundary between what it answers and what it escalates is the design, and it took iteration. Manufacturing enquiries are also technical, and a buyer asking about a specification will not accept a brochure paragraph. The last one is unglamorous: WhatsApp connectivity in production is fragile, sessions drop, and something running unattended for months has to be engineered for reconnection rather than for the happy path.

## Result
An enquiry at any hour gets a proper answer and arrives in the ERP as a qualified lead. What used to sit on somebody's personal phone is now a record the group can count and follow up.

## Verified evidence
The system runs in production at the group on both channels. Independently of the employer, I built and run a WhatsApp integration estate of my own under my own venture, with a documented send contract, a live product catalogue on a business-verified number and an unattended posting engine, which is the same capability on infrastructure I can demonstrate. I hold the conversation logs and can produce the conversation count and the after-hours share on request. I do not quote figures I have not measured.

## Skills demonstrated
Applied AI in production, conversational system design, WhatsApp and web channel integration, CRM and ERP integration, multi-brand architecture, unattended service reliability.

## Suitable target roles
Head of Digital and AI Transformation, IT Director, Senior Leader IT and AI Transformation.

## Three interview talking points
1. "An enquiry at two in the morning gets a proper answer and arrives in the ERP as a qualified lead. That is on WhatsApp and on the websites."
2. "The five AI systems are not five bolt-ons. Chat runs through one platform serving several numbers and all the websites, so adding a brand is configuration."
3. "The agent qualifies, it does not commit. Deciding what it must escalate was more of the work than making it talk."
