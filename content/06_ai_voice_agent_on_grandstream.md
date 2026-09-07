# An AI voice agent on the corporate phone system

## Situation
A manufacturing group with telephony across six sites, running on Avaya and Grandstream platforms. Telephony sits inside my IT function rather than with facilities or an outside supplier, which turns out to be the fact that made this project possible.

## Business problem
Calls outside office hours went unanswered. In a business selling into five countries, "outside office hours" covers a large part of the working week somewhere. A caller who reaches a ring tone does not leave a voicemail. They call the next supplier. There was also no record the call had happened, so the loss was invisible: you cannot review a report of calls nobody answered and nobody logged. Chat had already been solved. Voice is where people still go when the enquiry is urgent, and voice was the gap.

## My responsibility
I designed and built it, on a phone platform I already own and administer. It is one of five AI systems of my design in daily production at the group.

## Solution
An AI agent that answers and handles inbound calls on the Grandstream platform. It picks up, holds a conversation, deals with what it can deal with, and takes what it cannot to the right place instead of dropping it.

Most organisations that want this buy a hosted service and point their numbers at somebody else's cloud, which means a cost per minute, caller audio leaving the estate, and a dependency on a supplier's roadmap. Because the phone platform is mine and I administer it, I built the agent onto our own telephony rather than renting a service in front of it. Call handling stays inside the estate and the design stays under my control.

## Technology
Grandstream telephony, VoIP, speech and large language model APIs, Python, Linux, integration with the group's systems of record.

## Implementation
Built onto the existing VoIP estate rather than beside it, so numbers, extensions and routing carry on working as they did. Introduced first where an unanswered call was pure loss, with fallback behaviour defined before it went near a live number.

## Challenges
Voice is much less forgiving than chat. A pause of a second that nobody notices when typing is an awkward silence on a call, so latency is a design constraint from the first line of code rather than a tuning exercise at the end. Callers to a manufacturer in this region speak in a wide range of accents and several languages, often on a poor connection. Handover has to be clean too, because an agent that traps a caller in a loop is worse than the ring tone it replaced.

## Result
Calls that used to ring out are answered and handled, and voice stopped being the channel where enquiries disappeared.

## Verified evidence
The agent runs in production on the group's Grandstream platform, and my ownership of both the Avaya and Grandstream estates is what the build depends on. I hold the platform call records and can produce the calls-handled figure on request. I do not quote a number I have not measured. No recordings, transcripts or caller details are used in any write-up or demonstration.

## Skills demonstrated
VoIP and telephony administration, applied AI in production, speech interface design, latency-sensitive engineering, integration of AI with existing corporate infrastructure.

## Suitable target roles
Head of Digital and AI Transformation, IT Director, Head of IT.

## Three interview talking points
1. "We have an AI agent on the phone system, not only on chat. It answers and handles calls on Grandstream."
2. "It runs on our own telephony rather than a hosted service in front of it. That is only possible because the phone platform sits with IT."
3. "Latency is the whole design. On chat a second is nothing. On a call it is a silence, and the caller decides you are broken."
