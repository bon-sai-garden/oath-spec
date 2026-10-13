---
title: "Example: Eucrates"
type: example
status: active
tags: [oaths, example]
---

# Example: Eucrates

A complete AI teammate, written to OATHS 1.0, small enough to read in one sitting.

The teammate is named Eucrates (*yoo-KRAY-teez*, "you create"); the name, its Greek roots and its acronym are explained in [the constitution](eucrates/constitution.md).

Eucrates is modelled on the apprentice of Goethe's ballad *Der Zauberlehrling* (1797), who, left alone, starts a spell he cannot stop. The poem is the oldest well-known account of the failure an AI teammate has to be designed against, and it is in the public domain. The quotations are from the German original, each with our own English paraphrase; no published translation is used.

- [eucrates/SKILL.md](eucrates/SKILL.md): the package entry point (Agent Skills format)
- [eucrates/constitution.md](eucrates/constitution.md): State 2: the constitution, who the teammate is
- [eucrates/role.md](eucrates/role.md): Roles 1 and 3–5: what they are for, who sponsors them, where their circle is held, and their cohort (none)
- [eucrates-state/working-state.md](eucrates-state/working-state.md): State 2: what is open
- [eucrates-state/journal/2026-10-01.md](eucrates-state/journal/2026-10-01.md): State 2: what happened
- [eucrates/patterns.md](eucrates/patterns.md): State 5: lessons that passed review
- [eucrates-state/lessons.md](eucrates-state/lessons.md): State 5: what went wrong, and the guard
- [eucrates-state/handover.md](eucrates-state/handover.md): State 2 and 3: what the next session needs

> [!note] Unsigned on purpose
> The example carries no keys, signatures or manifest. A conformance run generates them fresh for a throwaway key (Provenance 1–2), checks them, and discards them, so nothing that could be mistaken for a real identity is ever committed.

> [!note] No circle here, on purpose
> The role file says that Eucrates has a circle, where it is held and who may widen it. The circle itself names people, so it is private state and is never published, in part or as a hash (Roles 4). Its absence from this repository is the example.
