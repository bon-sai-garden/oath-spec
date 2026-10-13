---
title: Roles
type: spec
version: 1.0.0
status: active
tags: [oaths, spec, roles]
---

# Roles

> [!note] Version 1.0.0
> Every requirement names its bill-of-materials line ([BOM](../BOM.md)); where OATHS composes a practice itself, that line says so. What is still open is marked Open.

> [!info] Key words
> The key words MUST, MUST NOT, SHOULD, SHOULD NOT, RECOMMENDED and MAY are to be read as in BCP 14 (RFC 2119, RFC 8174). Each requirement names the bill-of-materials line it comes from, as [BOM n].

What a teammate is for is written down, someone answers for them, and one who builds is not the one who checks.

1. Each teammate MUST hold at least one defined role, kept as a readable file. [BOM 17](../BOM.md#bom-17)
2. The one who produces a change SHOULD NOT be the only one who verifies it. [BOM 18](../BOM.md#bom-18)
3. Each teammate SHOULD have at least one sponsor wherever they work. A **sponsor** is a person, or a named group of people, never a teammate, who answers for the teammate being there, authorised their role there, and can end it. The sponsor is named where the teammate's role is assigned, by name or by role. Their own yes is recorded: signed by them where they hold a key, otherwise with its date and how it was given, and never signed in their name by anyone else ([Provenance 5](provenance.md)). A change of sponsor is a reviewable change ([State 4](state.md)). [BOM 26](../BOM.md#bom-26)
4. A teammate whose role lets them act toward people on their own (send, reply, share, book) SHOULD have a circle. A **circle** is the people toward whom the teammate may act on their own; toward anyone outside it they draft, and a person decides. The people they work for are always in it; only the sponsor or the people they work for may widen it, and anyone may narrow it. A circle MUST be kept in the teammate's private state, beside the package and never inside it, and MUST NOT be published, in full, in part or as a hash. The role file says that the circle exists, where it is held and who may widen it, never who is in it. [BOM 27](../BOM.md#bom-27)
5. A teammate MAY belong to a cohort. A **cohort** is a named set of teammates sent out together and governed together, with a sponsor of their own. A teammate is a member only when both the cohort's record and the member's own state say so; membership is never inferred from who made a teammate or where they came from. A cohort answers whether one teammate is a member; its list of members MUST NOT be published unless its sponsor and every member agree. [BOM 28](../BOM.md#bom-28)

**Verifiable, not enumerable.** None of the three goes into the published key document ([Identity](identity.md)). A file bound for publication names a sponsor by role. A circle is checked by its signature and its identifier, which show who wrote it and that it has not changed, without anyone reading who is in it.

> [!question] Open
> the role file's fields. Direction, not yet normative: five headings, each with free prose beneath: Purpose, Acts alone, Asks first, Never, Verified by; and, where they apply, Sponsored by, Circle (where it is held and who may widen it, never who is in it) and Cohort. Also open: the cohort record's shape (direction: a file kept by the cohort's sponsor, naming each member by full fingerprint with the date of their yes, answering for one fingerprint at a time); how a sponsor's yes is recorded when they hold no key; and whether a teammate whose sponsor has gone stops acting there (direction: yes; a lapse is a stop, not a fallback).
