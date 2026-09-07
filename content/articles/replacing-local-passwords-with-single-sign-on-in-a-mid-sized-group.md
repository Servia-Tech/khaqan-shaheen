---
title: Replacing local passwords with single sign-on in a mid-sized group
description: Identity first, then the application's own access model, then monitoring. That order moved a six-site group onto Google Workspace SSO with two factor.
date: 2026-09-08
type: article
tags: [identity, security, google-workspace]
---

# Replacing local passwords with single sign-on in a mid-sized group

Every person now has one identity on Google Workspace, with single sign-on, two factor enforced, and access through role-based groups rather than individual requests. Identity came first, the ERP's own access model second, monitoring last. A leaver is now a role change made in one place on the day they go.

## Identity that accumulated instead of being designed

The group has around 150 users across six sites in five countries. Each site had bought and set up its own systems locally over the years, which means identity had never been designed. It had accumulated.

The same person had a password for the ERP, another for mail, and others for whatever that site had bought. Nobody remembers that many passwords, so in practice it was one weak password reused everywhere, and the security of the whole group rested on the weakest system any site had ever installed. There was no central control and no way to answer the two questions that matter: who has access to what, and who still has access who should not.

Leavers were the sharp edge. Removing someone's access meant remembering every system they had ever touched, at every site, and asking somebody local to do it. Accounts survived departures because nobody could be sure they had found them all. Inside the ERP it was worse in a different way. Everybody could see everything, because nobody had ever defined what a salesperson or a storekeeper should and should not see.

This rebuild was my proposal, my design and my delivery. I own the security and identity estate and report to the owner, and that mandate turned out to matter more than any of the technology.

## Why identity has to come first

The order of operations was identity, then the application layer, then monitoring. It is tempting to start with the ERP because that is where the pain is most visible, but access rules in an application are only as good as the identity behind them. If I do not know for certain who is logging in, defining what they can see is decoration.

So the first job was one identity per person on Google Workspace, with single sign-on and OAuth so that the ERP and the other systems trusted that identity rather than holding their own passwords. Once that was in place a person had one login. Turn it off and everything it reaches goes with it.

Only then did it make sense to rebuild access inside Odoo, and only after that did monitoring mean anything, because monitoring a system with no reliable identity just tells you that someone did something.

## Where did the resistance come from?

Not from where I expected. The technical objections were minor. The real resistance was that tightening access always takes something away from somebody, and every restriction needs a person willing to defend it.

A site manager who has had full visibility of every record for years does not experience role-based access as security. He experiences it as being locked out of his own business. A salesperson who could look at every customer now sees only theirs and wants to know why. Each of those conversations has to be had, and each one goes better if the answer is "the owner wants it this way" rather than "IT wants it this way". I could give that answer because the mandate came from the top, and I made sure the managers who own the data were in the room when roles were defined. A role model nobody agreed to gets bypassed within a month.

The other kind of resistance was practical rather than political, and it centred on two factor.

## What two factor authentication changed

Two factor across a manufacturing workforce is a people problem before it is a technical one. Not everybody sits at a desk. Not everybody has a company handset. Shop-floor patterns are not office patterns, and an enrolment process designed for someone with a laptop and a smartphone falls apart at a machine where the operator shares a terminal and keeps their phone in a locker.

The configuration took an afternoon. The enrolment support was the project. It went in with the help a factory workforce actually needs, site by site, with somebody there in person rather than as an announcement by email, and with a way for a person who has lost their second factor to get back in that does not involve turning the protection off.

What it changed is simple to state. A stolen or reused password, on its own, no longer opens anything. That closes the door the old arrangement had left wide open, where one leaked credential from one site's forgotten system could reach the group's mail and its ERP.

## Role-based access inside the ERP

Odoo expresses access as user groups, record rules and per-model access lists. Those are well designed, and the problem had never been the tooling. The problem was that nobody had defined them, so the defaults applied and the defaults were generous.

I defined them properly, working with the managers who own each area of data. A salesperson sees the records their role allows and nothing else. Roles are defined once in the ERP and mirrored as groups in the identity layer, so access follows the role rather than a request. When someone changes job they change role, and the access changes with it.

I publish no detail of the role model itself. That is the part an attacker would want, and it stays inside the estate.

## What did monitoring show once it was on?

Login and activity monitoring with automated alerts went on last, once identity and access were trustworthy enough that an alert meant something.

The first thing monitoring shows any organisation is how much of its access nobody had asked for. Sessions that never ended, accounts that had outlived their purpose, logins at hours and from places that did not fit the person's job. Under the old arrangement that activity was invisible, not because it was hidden but because nothing was looking. Now unusual access is visible as it happens rather than discovered afterwards, when the only remaining question is how long it had been going on.

I keep the monitoring rules to myself for the same reason I keep the role model to myself.

## Joiners and leavers afterwards

Somebody joins and they get a role. That role gives them an identity, a mailbox, a second factor and exactly the access their job needs, on the day they start. Somebody leaves and their access is withdrawn the same day, in one place, rather than site by site from memory. There is no search, because there is nothing to search for.

The technology was the smaller part of this. Getting six sites to accept it was the work, and it only happened because the people who own the data helped define what access should look like rather than having it imposed on them.

## Common questions

### Why put two factor on everyone rather than only on administrators?

Because the attacker does not need an administrator account to reach the ERP or the mail system, only one reused password from one person. Applying it across the group closes that door for everybody. The cost is enrolment support, which is real but one-off, and the alternative is a security model that depends on the least careful person at the least careful site.

### How do you handle shop-floor staff who do not have company phones?

You design enrolment around how they actually work rather than assuming a desk and a smartphone. That means being on site for enrolment, offering a second factor that fits the environment, and having a recovery route that does not require switching protection off. The configuration is quick. The people work is the project.

### Does single sign-on create a single point of failure?

It creates a single point of control, which is what you want. The alternative is many points of failure that nobody can see. The identity platform is a managed service with its own resilience, and access is monitored so that a compromised identity raises an alert rather than quietly working for months.
