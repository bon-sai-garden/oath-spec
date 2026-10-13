---
title: What a reference implementation must show
type: guide
status: active
tags: [oaths, implementing]
---

# What a reference implementation must show

> [!note] Version 1.0.0
> Where the reference implementation lives is not decided; this says only what it must do. It must be small enough to read in one sitting, and it must name no teammate, person or place.

A reference implementation is a tool server the harness talks to over the Model Context Protocol [BOM 24](BOM.md#bom-24). It shows each OATHS section working once, end to end, on a throwaway example team that its tests generate fresh on every run and never ship: fresh keys, generic names. No real team, and so no real name, can ever reach it by construction.

## The five things it shows

1. **Session start, integrity first** (Conformance 1). The first call a teammate makes returns an `integrity:` line before anything else: their package's manifest verified [Provenance 2](spec/provenance.md), their own signatures verified, and their fingerprint compared in full [Identity 3](spec/identity.md). Anything but a pass stops the session, with the reason named, and no other tool answers.
2. **Their own handover, and nobody else's** (State 3). The session-start call returns the newest handover whose owner is the calling teammate. A handover owned by another is never returned, whatever its name or date.
3. **Resolution by identifier** (Conformance 2). A document is fetched by its stable id, not by a path. A moved document is still found; an id that names nothing is a refusal.
4. **Verified memory** (Provenance 1, State 1). Every state file the server returns has had its detached signature checked first; a file whose signature fails is not returned, and the reason is.
5. **A signed write** (Provenance 1, 4, 5). A write by a teammate is signed by that teammate, as custodian where the file credits someone else, with the key never leaving custody.

Roles 3 to 5 (sponsor, circle, cohort) are not required of every teammate, so they are not among the five. Where the example team has them, the server shows them working: a sponsor named where the role is assigned; a circle returned only to its own teammate, never inside a package and never to another caller; and a cohort that answers, for one fingerprint at a time, whether that teammate is a member.

## How it is checked

- A conformance suite runs each of the five against the example team, and each check has been seen to fail on a planted fault [Conformance 3](spec/conformance.md). Part 1 (identity and provenance) exists: `node conformance/run.mjs`. Part 2 runs the session checks against an implementation.
- The fence check passes on the implementation's own tree.

## Open

- Where it lives, and its name.
