"""Topic-specific reading aids and original explanatory SVGs for the editorial library."""
import html
import math
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).parent
E = html.escape
# Editorial examples explain decisions; they do not introduce new personal results.
TOPICS = {
 'erp': ('One set of records', 'Order → production → delivery → invoice', ['Customer order', 'Production plan', 'Stock movement', 'Financial record'], 'An integration is an operational commitment, not just a launch task.', 'Before adding another system, trace one real order through every hand-off. Write down who owns the record when two screens disagree.', 'manufacturing'),
 'database': ('A migration is a recovery plan', 'Rehearse → synchronise → validate → switch', ['Rehearsal clone', 'Data synchronisation', 'Validation gate', 'Controlled cutover'], 'The rollback decision belongs in the runbook before the cutover starts.', 'Ask the team to demonstrate a restore, then time a complete business transaction on the restored application. A backup file alone does not answer either question.', 'strategy'),
 'ai': ('Where automation meets accountability', 'Input → bounded action → review → record', ['Business input', 'Bounded AI task', 'Human decision', 'Auditable record'], 'A fluent answer is not evidence that a business action is correct.', 'Pick one failure case: the connection drops after a record is created. Decide how a retry finds that record instead of creating it again.', 'consulting'),
 'identity': ('A login is only the first gate', 'Identity → second factor → role → record', ['Known identity', 'Second factor', 'Application role', 'Permitted records'], 'Authentication and authorisation answer different questions.', 'Test the same record with a finance user, a plant user and a disabled account. Check access to the underlying record, not only whether a menu is hidden.', 'strategy'),
 'factory': ('Opening day starts with dependencies', 'Connectivity → identity → ERP → floor test', ['Working circuits', 'User identities', 'Site configuration', 'Real floor test'], 'A printer that works in the office has not passed the shop-floor test.', 'Walk one transaction from the gate to dispatch using the actual scanner, label stock, network and user account that will be used on opening day.', 'manufacturing'),
 'ocr': ('Reading is not validating', 'Document → extraction → checks → review', ['Original document', 'Structured fields', 'Business checks', 'Review queue'], 'The dangerous error is a wrong amount that still looks plausible.', 'Try a duplicate invoice, a missing currency and a total obscured by a stamp. A successful test routes each exception deliberately; it does not guess.', 'consulting'),
 'search': ('Can the answer be found?', 'Discover → fetch → understand → measure', ['Discover the URL', 'Fetch the page', 'Read the evidence', 'Measure referrals'], 'Crawler access is a prerequisite, not a promise of a citation.', 'Open the raw HTML and find the sentence that answers the customer’s question. Then check whether its supporting evidence is visible and linked.', 'strategy'),
 'scheduling': ('One machine, one commitment', 'Choose → calculate → check → reserve', ['Choose a machine', 'Calculate interval', 'Check overlaps', 'Reserve atomically'], 'Two valid-looking requests can still collide when they arrive together.', 'Submit two overlapping orders at the same time in a test environment. The system must reject one consistently, rather than relying on a planner to notice.', 'manufacturing'),
 'sales': ('A conversation should become a usable lead', 'Message → qualify → hand off → CRM', ['Customer message', 'Bounded qualification', 'Human hand-off', 'ERP lead'], 'A lead needs a traceable next action, not just a transcript.', 'Ask for an unavailable product, then ask for a person. The agent should respect catalogue limits and make a clean hand-off without promising stock or prices it cannot verify.', 'consulting'),
 'voice': ('Make the hand-off audible', 'Call → intent → boundary → transfer', ['Incoming call', 'Identify intent', 'Respect boundaries', 'Human transfer'], 'The fallback matters most when speech recognition is least certain.', 'Test background noise, an interrupted sentence and a request for a human. Listen to the complete transfer experience, including the moment the automated agent stops.', 'consulting'),
 'attendance': ('From a device event to a payroll record', 'Capture → match → validate → approve', ['Attendance event', 'Employee mapping', 'Exception review', 'Payroll input'], 'A device event and an approved attendance record are different things.', 'Use a test employee with a missed punch and a cross-midnight shift. Check time-zone handling and the exception trail before the result reaches payroll.', 'manufacturing'),
 'patrol': ('A checkpoint needs context', 'Checkpoint → evidence → validation → review', ['Assigned checkpoint', 'Time and location', 'Validation checks', 'Supervisor review'], 'A location reading is one signal; it is not the whole patrol.', 'Test a missed checkpoint and an unavailable location signal. Keep the distinction between a failed validation and a completed patrol visible to the reviewer.', 'manufacturing'),
 'measurement': ('Make a number defensible', 'Question → baseline → window → method', ['Clear question', 'Comparable baseline', 'Defined time window', 'Repeatable method'], 'A percentage without a denominator is an unfinished explanation.', 'Write the claim, the date range, the sample size and the exclusions on one card. If another person cannot reproduce the count, keep it as a hypothesis.', 'boardroom'),
 'venture': ('Follow the customer all the way through', 'Visit → booking → delivery → feedback', ['Customer visit', 'Booking intention', 'Service delivery', 'Operational feedback'], 'A dashboard is useful when it changes the next decision.', 'Trace a single enquiry from the landing page to the promised reply. Look for the quiet gap where a customer can wait while every individual system still reports success.', 'consulting'),
}

ENTRIES = {
 'why-i-extended-one-erp-instead-of-buying-a-second-system': ('erp', 'The expensive part of a second system starts after the interface goes live.'),
 'a-postgresql-upgrade-nobody-was-allowed-to-notice': ('database', 'The database version was the visible change. Keeping the business working was the real assignment.'),
 'five-ai-systems-in-production-what-breaks-when-nobody-is-watching': ('ai', 'The demo ends. The connection drops. Who notices, and what happens next?'),
 'replacing-local-passwords-with-single-sign-on-in-a-mid-sized-group': ('identity', 'One sign-in can simplify life. It cannot decide which invoices a person should see.'),
 'bringing-a-new-factory-online-the-order-of-operations': ('factory', 'A factory can look ready while the first label still cannot print.'),
 'check-whether-chatgpt-perplexity-and-google-ai-overviews-can-read-your-website': ('search', 'Before optimising for an AI answer, check whether the answer is actually on your page.'),
 'how-to-write-an-llms-txt-for-a-business-website': ('search', 'Think of llms.txt as an optional reading map. The real evidence still lives on the linked pages.'),
 'google-workspace-single-sign-on-for-odoo-and-two-factor-authentication': ('identity', 'Start with a test account and a recovery path, then work through the access model.'),
 'odoo-stop-two-work-orders-booking-the-same-machine': ('scheduling', 'The second planner clicks Save a fraction of a second later. Does your check still hold?'),
 'reading-supplier-bills-into-an-erp-with-an-llm-ocr-pipeline': ('ocr', 'A readable invoice is not necessarily a payable invoice.'),
 'whatsapp-ai-sales-agent-that-hands-leads-to-your-erp': ('sales', 'The useful outcome is a qualified lead somebody can act on, not an endless conversation.'),
 'zero-unplanned-downtime-postgresql-major-upgrade-checklist': ('database', 'Rehearse the decision to stop as carefully as the decision to switch.'),
 'the-month-end-test-for-erp-health': ('erp', 'Ask finance how the month closes. The answer reveals where the records stop agreeing.'),
 'what-i-check-the-week-before-a-factory-opens': ('factory', 'A week before opening, a real test beats another green status slide.'),
 'what-ocr-gets-wrong-on-supplier-bills': ('ocr', 'The model picked a number. Was it the total, the tax, or a correction in the margin?'),
 'what-running-my-own-venture-taught-me-about-corporate-it': ('venture', 'Owning the bill changes the questions you ask about the system.'),
 'why-every-ai-agent-i-run-sits-behind-a-human-queue': ('ai', 'The review queue is where a plausible machine output becomes an accountable business decision.'),
 'why-i-published-my-case-studies-without-numbers': ('measurement', 'An impressive percentage should survive one ordinary question: how did you count it?'),
 'machine-scheduling-and-overlap-prevention': ('scheduling', 'A factory schedule needs a rule that survives simultaneous bookings.'),
 'one-erp-six-sites-five-countries': ('erp', 'Six sites should not need six versions of the truth.'),
 'postgresql-9-5-to-16-migration': ('database', 'A major upgrade earns its value when the people using the system can keep working.'),
 'document-ocr-into-the-erp': ('ocr', 'The document is the starting point. A checked record is the destination.'),
 'ai-sales-agent-whatsapp-and-web': ('sales', 'An enquiry at midnight still needs a clear owner in the morning.'),
 'ai-voice-agent-on-grandstream': ('voice', 'A useful voice agent knows when the next voice should be a person.'),
 'identity-and-access-rebuild': ('identity', 'Access should follow a person’s job, not the history of their passwords.'),
 'multi-site-biometric-attendance': ('attendance', 'The hard part begins after the device records the punch.'),
 'geo-verified-security-patrol': ('patrol', 'Make the evidence behind a completed checkpoint inspectable.'),
 'bringing-a-new-factory-online': ('factory', 'Opening-day readiness is the result of testing the entire chain.'),
}

SOURCES = {
 'database': ('Technical fact', 'PostgreSQL 16 logical replication does not copy schema changes or sequence state. Both need an explicit migration step.', 'PostgreSQL 16: logical replication restrictions', 'https://www.postgresql.org/docs/16/logical-replication-restrictions.html'),
 'search': ('Search fact', 'Google says AI Overviews and AI Mode require no special additional optimisation. Eligibility still depends on indexing and snippet access; inclusion is not guaranteed.', 'Google Search Central: AI features', 'https://developers.google.com/search/docs/appearance/ai-features'),
 'identity': ('Access fact', 'Odoo separates access rights from record rules. Signing in successfully does not define which business records a person may access.', 'Odoo 17: access rights', 'https://www.odoo.com/documentation/17.0/applications/general/users/access_rights.html'),
 'scheduling': ('Database fact', 'PostgreSQL range types can express time intervals; exclusion constraints can prevent overlapping reservations.', 'PostgreSQL 16: range types and constraints', 'https://www.postgresql.org/docs/16/rangetypes.html'),
}

def illustration(slug):
    return f'/assets/img/editorial/{slug}.svg'

def make_visuals():
    directory = ROOT/'assets/img/editorial'
    directory.mkdir(exist_ok=True)
    colors=['#62f4d2','#6cbcff','#c9a1ff','#ffc98b']
    for n,(slug,(topic,hook)) in enumerate(ENTRIES.items()):
        title,route,nodes,_,_,_=TOPICS[topic]
        accent=colors[n%len(colors)]
        # Original explanatory diagram: four numbered stages and their connections.
        shape=''
        for i,(x,y) in enumerate([(205,160),(805,160),(205,420),(805,420)]):
            shape+=f'<rect x="{x-105}" y="{y-83}" width="390" height="165" rx="20" fill="#102235" stroke="{accent}" stroke-opacity=".5"/><circle cx="{x-42}" cy="{y}" r="28" fill="{accent}"/><text x="{x-42}" y="{y+10}" text-anchor="middle" fill="#07121c" font-family="Arial,sans-serif" font-weight="700" font-size="30">{i+1}</text>'
            for j,label in enumerate(textwrap.wrap(nodes[i],width=16)):
                shape+=f'<text x="{x+6}" y="{y-8+j*38}" fill="#e5f3ff" font-family="Arial,sans-serif" font-size="29">{E(label)}</text>'
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" role="img" aria-labelledby="title desc"><title id="title">{E(title)}</title><desc id="desc">{E(" → ".join(nodes))}. Four stages, numbered in order.</desc><defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M 40 0 L 0 0 0 40" fill="none" stroke="#254157" stroke-width="1"/></pattern><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="{accent}"/></marker></defs><rect width="1200" height="600" rx="20" fill="#091522"/><rect width="1200" height="600" fill="url(#grid)" opacity=".5"/><path d="M500 160H690 M1100 160H1150V300H60V420H90 M500 420H690" fill="none" stroke="{accent}" stroke-width="3" stroke-dasharray="8 8" opacity=".7" marker-end="url(#arrow)"/>{shape}<text x="600" y="579" text-anchor="middle" fill="#9eb3c9" font-family="Arial,sans-serif" font-size="20" letter-spacing="4">KHAQAN SHAHEEN / FIELD NOTES {n+1:02}</text></svg>'
        (directory/f'{slug}.svg').write_text(svg,encoding='utf-8')

def card_image(slug):
    if slug not in ENTRIES:return ''
    return f'<img class="editorial-thumb" src="{illustration(slug)}" alt="" width="1200" height="600" loading="lazy" decoding="async">'

def reading(slug, rendered, words):
    if slug not in ENTRIES:return rendered
    topic,hook=ENTRIES[slug]
    title,route,nodes,takeaway,exercise,photo=TOPICS[topic]
    headings=[]
    def heading(m):
        text=re.sub('<[^>]+>','',m.group(1))
        anchor=f'read-{len(headings)+1}'
        headings.append((anchor,text))
        return f'<h2 id="{anchor}">{m.group(1)}</h2>'
    rendered=re.sub(r'<h2>(.*?)</h2>',heading,rendered,flags=re.S)
    toc='<details class="reading-toc"><summary>In this '+('note' if words<550 else 'story')+'</summary><ol>'+''.join(f'<li><a href="#{a}">{t}</a></li>' for a,t in headings)+'</ol></details>' if headings else ''
    brief=f'<div class="reading-topline"><span>FIELD NOTES / {E(topic.upper())}</span><span>{max(1,math.ceil(words/200))} min read</span></div><p class="reading-hook">{E(hook)}</p><aside class="reading-brief"><span class="eyebrow">The idea to take away</span><p>{E(takeaway)}</p></aside>'
    visual=f'<figure class="editorial-figure"><img src="{illustration(slug)}" alt="{E(title)}: {E(route)}" width="1200" height="600" fetchpriority="high"><figcaption><strong>{E(title)}</strong><span>Concept diagram. Read the four stages below.</span></figcaption></figure><ol class="reading-stages">'+''.join(f'<li><span>{i+1:02}</span>{E(t)}</li>' for i,t in enumerate(nodes))+'</ol>'
    practice=f'<aside class="reading-practice"><span class="eyebrow">Try this with your team</span><p>{E(exercise)}</p></aside>'
    fact=''
    if topic in SOURCES:
        label,text,name,url=SOURCES[topic]
        fact=f'<aside class="reading-fact"><span class="eyebrow">{label}</span><p>{E(text)}</p><a href="{url}">{E(name)} ↗</a><small>Documentation checked 10 September 2026.</small></aside>'
    # Insert a visual break into the narrative, before the third major section.
    if len(headings)>2:
        target=f'<h2 id="{headings[2][0]}">'
        rendered=rendered.replace(target,fact+target,1)
        fact=''
    demo=demo_html(topic)
    # Photographs are existing illustrative assets, not asserted to be site evidence.
    photograph=''
    if words>=850:
        photograph=f'<figure class="editorial-photo"><img src="/assets/img/photos/{photo}-800.jpg" srcset="/assets/img/photos/{photo}-800.jpg 800w, /assets/img/photos/{photo}-1400.jpg 1400w" sizes="(max-width:800px) 100vw, 800px" alt="Illustrative {photo} scene accompanying this technology article" width="1400" height="933" loading="lazy" decoding="async"><figcaption>Illustrative scene. The case evidence is described in the text.</figcaption></figure>'
    return brief+toc+'<div class="reading-body">'+visual+rendered+fact+demo+photograph+practice+'</div>'

def demo_html(topic):
    if topic in ('ocr','ai','measurement'):
        return '''<section class="reading-demo" data-demo="review"><span class="eyebrow">Interactive example · hypothetical data</span><h2>What does “95% correct” leave for a person?</h2><p>Change the volume and first-pass accuracy. This calculates review workload, not measured performance of my systems. A correct extraction still needs business validation.</p><div class="demo-controls"><label>Documents per month<input name="volume" type="range" min="100" max="10000" step="100" value="1000"><output data-volume>1,000</output></label><label>Correct on first pass<input name="accuracy" type="range" min="50" max="100" value="95"><output data-accuracy>95%</output></label></div><div class="demo-bars" aria-hidden="true"><span data-clean style="width:95%"></span><span data-review style="width:5%"></span></div><p class="demo-result" role="status"><strong data-result>50 documents</strong> need correction in this example.</p><p class="small muted">Formula: volume × (1 − accuracy / 100). Default: 1,000 × 5% = 50.</p><noscript><p>The initial example is shown above; enable JavaScript to change the inputs.</p></noscript></section>'''
    if topic=='scheduling':
        return '''<section class="reading-demo" data-demo="schedule"><span class="eyebrow">Interactive example · one machine</span><h2>Would these two orders collide?</h2><p>Order A runs from 09:00 to 11:00. Order B lasts two hours. Move its start time to test the overlap rule.</p><label>Order B start<input name="start" type="range" min="8" max="14" step="0.5" value="10"><output data-start>10:00</output></label><div class="schedule-line"><span style="left:12.5%;width:25%">A</span></div><div class="schedule-line"><span data-order style="left:25%;width:25%">B</span></div><p class="demo-result" role="status" data-result>Conflict: both orders use the machine from 10:00 to 11:00.</p><p class="small muted">Demonstration assumes half-open intervals [start, end): a job may start when the previous one ends. Add setup time if your process requires it.</p></section>'''
    if topic=='database':
        return '''<aside class="reading-fact"><span class="eyebrow">Three separate checks</span><h2>“Caught up” does not mean “ready”.</h2><div class="table-scroll" tabindex="0" role="region" aria-label="Migration readiness checks"><table><thead><tr><th>Check</th><th>What it answers</th></tr></thead><tbody><tr><td>Row synchronisation</td><td>Have changes reached the target?</td></tr><tr><td>Schema and sequences</td><td>Will the next write work correctly?</td></tr><tr><td>Application transaction</td><td>Can a real user complete the business process?</td></tr></tbody></table></div><p>These are distinct acceptance gates, not a measured migration timeline.</p></aside>'''
    if topic=='erp':
        return '''<aside class="reading-fact"><span class="eyebrow">Published project scope</span><div class="scope-strip"><div><strong>6</strong><span>sites</span></div><div><strong>5</strong><span>countries</span></div><div><strong>1</strong><span>ERP instance</span></div></div><p>Scope reported in <a href="/work/one-erp-six-sites-five-countries.html">my ERP case study</a>. These are deployment counts, not a claim about time or money saved.</p></aside>'''
    return ''
