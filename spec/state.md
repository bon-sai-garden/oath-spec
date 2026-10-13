---
title: State
type: spec
version: 1.0.0
status: active
tags: [oaths, spec, state]
---

# State

> [!note] Version 1.0.0
> Every requirement names its bill-of-materials line ([BOM](../BOM.md)); where OATHS composes a practice itself, that line says so. What is still open is marked Open.

> [!info] Key words
> The key words MUST, MUST NOT, SHOULD, SHOULD NOT, RECOMMENDED and MAY are to be read as in BCP 14 (RFC 2119, RFC 8174). Each requirement names the bill-of-materials line it comes from, as [BOM n].

A teammate's continuity lives in plain files they read at the start of a session, and in nothing they cannot show.

1. A teammate's state MUST be kept in plain, versioned files that they read at session start. [BOM 13](../BOM.md#bom-13)
2. State SHOULD be layered in five slots: a constitution (who the teammate is), a working state (what is open), a journal (what happened), a handover (what the next session needs) and lessons (what went wrong, and the guard that now prevents it). [BOM 14](../BOM.md#bom-14), [BOM 25](../BOM.md#bom-25)
3. A session MUST receive only its own teammate's handover, never another's. [BOM 15](../BOM.md#bom-15)
4. A teammate's memory is their own to write. A change to a file that fixes their identity or their strategy (their constitution, for example) SHOULD be a reviewable change that a human can veto, and such files SHOULD be reviewed again from time to time, not only when they change. Who decides is not specified. [BOM 16](../BOM.md#bom-16)
5. Every failure SHOULD leave a lesson: what went wrong, the guard added, and evidence that the guard was seen to fail. The guard SHOULD sit where the harness can enforce it (a rule in the instruction file, a check, a test or a tool), not only in the record. A lesson that should change every session's behaviour SHOULD be promoted, after review, into the instruction file or into a patterns file that the instruction file names, through the same reviewable, vetoable change as rule 4. [BOM 25](../BOM.md#bom-25), [BOM 19](../BOM.md#bom-19)

> [!question] Open
> the slot names on disk, and how a slot declares its owner. Direction, not yet normative: the names are fixed (`constitution.md`, `working-state.md`, `journal/`, `handover.md`, `lessons.md`, `patterns.md`), and a package may name its constitution `SOUL.md`, a name in use in OpenClaw's docs, as an alias for the same slot, with one real file and at most a pointer. State that changes during a session is meant to live beside the signed package and not inside it, because a signed file cannot change without breaking its signature. A teammate's circle ([Roles 4](roles.md)), where they have one, is state of this kind, and private: it is never in the package and never published.
