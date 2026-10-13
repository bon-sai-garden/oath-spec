# AGENTS.md — OATHS

> [!note] Home and visibility
> Two repositories, one specification. **`bon-sai-garden/oath-spec`** is production: the public home, public at launch. **`bon-sai-garden/oaths`** is staging: the work happens there, and oath-spec receives a cut of it. Nothing is published before the owner has read the cut tree; that review happens on the tree that will be committed, not on a working copy.

## The fence — every change is checked against it

This repository will be public. It must read as generic and technical. Before any commit:

- **No names** of people, households, employers, clients, hosts or cities.
- **No instance material** from any team: no named agents, personas, crews, rosters, agent packages, memory, letters or transcripts. OATHS specifies slots, never what fills them.
- **No private identifiers**: no fingerprints, keys, salts, emails or internal ticket numbers.
- **Every practice has a source.** A line in BOM.md without prior art does not belong here.
- **Third-party material is credited** in CREDITS.md, with its licence.

Run `python3 tools/fence-check.py . --deny <list>` before any commit bound for publication. The owner ruled on 2026-10-16 that the public home on line 4 stays named: add `--allow-at AGENTS.md:4`. The script names no one: the terms it guards live in a private deny list kept outside this repository. Without `--deny` it still checks emails, fingerprints, ticket ids and secret-shaped names, and says the names were not checked. A human read stays the last step.

## Decided (the owner, 2026-09-29)

- Licence: Apache 2.0 for the specification text and the code alike.
- The reference implementation is maintained in a separate project; its link is added at publication.
- "One master" (Conformance 4): MUST for trust material, SHOULD for everything else.

## Open

- The trackback registry (a later release).
