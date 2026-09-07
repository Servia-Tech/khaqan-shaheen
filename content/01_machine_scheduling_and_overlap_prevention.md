# Machine scheduling and order-overlap prevention in a manufacturing ERP

## Situation
A plastics manufacturing group running six sites across five countries on one Odoo ERP that I implemented and whose custom development I own and direct. Machines are the constraint. Every promise to a customer is really a promise about a machine being free.

## Business problem
Scheduling happened outside the system, in planners' own working notes. Nothing stopped two work orders being committed to the same machine for the same window, and nobody found out at the point of booking. They found out on the shop floor, with material staged and an operator waiting, after sales had already given the customer a date.

## My responsibility
I own the ERP function and I own and direct its custom development. This was mine end to end as the owner: I specified the data model, the Python and the views, reviewed the build, ran the testing and the rollout to planners on shifts.

## Solution
I modelled the machines first. Each carries a capacity type and a capacity figure, and work orders are assigned to a named machine rather than a vague work centre. Shifts are records, so a long order splits across shifts on the real shift length. Duration and end date are then calculated rather than typed, from quantity, machine capacity, machine start and stop time and the shift boundaries.

On top sits the guard. Three points in the booking flow check whether the machine is already committed for that window. If it is, the save is refused, with an error naming the conflicting work order and its manufacturing order. For clashes already sitting in live data I added a computed conflict count with a drill-through that opens them, so a planner sees a number and clicks it. Machine change and order split are controlled wizards, so a re-plan recalculates the dependent dates instead of moving a label.

## Technology
Python, the Odoo ORM, computed fields and server-side constraints, XML views and wizards, QWeb, JavaScript, PostgreSQL, Linux.

## Implementation
Built incrementally against real planning data. The conflict count shipped before the hard block, so planners could clear the existing clashes before the system began refusing saves.

## Challenges
Retrofitting a rule into a live plant is the hard part. A blocking constraint that is slightly wrong stops production, so the guard had to be right about split orders, machine changes mid-run and orders that legitimately share a window. An error saying only "machine busy" also gets worked around, which is why the message names the other order.

## Result
Double-booking is refused at save time rather than discovered on the floor. End dates are calculated. A plan change recalculates the dates that depend on it.

## Verified evidence
`gt_order_mgnt/models/mrp_machine.py`, 2,990 lines, in a custom Odoo module tree I hold. Three separate machine-busy guards raise a user-facing error naming the conflicting work order and manufacturing order. A computed conflict-count field with its compute method, and an action that opens the conflicting orders. Machine change and order split exist as wizards. The code is my employer's and is not published here.

## Skills demonstrated
Manufacturing process modelling, capacity planning and machine scheduling, Odoo module engineering, server-side constraint design, working with shop-floor users.

## Suitable target roles
IT Director in manufacturing, Head of IT, ERP Manager, Digital Transformation Manager.

## Three interview talking points
1. "The system refuses to save a work order that overlaps another on the same machine. Before that, we found out on the shop floor."
2. "I shipped the conflict count before the hard block. Turning a rule on in a live plant is a sequencing problem, not a coding problem."
3. "The end date is calculated from quantity, capacity, start and stop time and shift length, not typed in by a planner."
