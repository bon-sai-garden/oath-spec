# OATHS — Open Agentic Teammate Harness Specification

OATHS specifies an **AI teammate**: an agent that works alongside people over many sessions, with their own identity, a defined role, state they carry from one session to the next, and work that can be checked for who made it.

It is a bill of material (BOM) and the **least common denominator**. A teammate written to OATHS uses only what every capable agent harness already offers, such as files read at the start of a session, packaged skills and tools over the Model Context Protocol. So it runs unchanged on many harnesses. Anything specific to one harness goes into an **add-on**, layered on top and never required.

OATHS is **packaging, not invention**: a bill of materials of well-known practice, each line naming its prior art. It is technical and neutral. It defines slots and formats, never what fills them.

## Contents

| | |
|---|---|
| [spec/overview.md](spec/overview.md) | what OATHS is, what it isn't, and how add-ons layer on |
| [spec/anatomy.md](spec/anatomy.md) | the anatomy of an AI teammate: the ingredients, their sources, and where existing harnesses already carry them |
| [spec/](spec/) | the specification: identity, provenance, state, roles, conformance |
| [spec/harnesses.md](spec/harnesses.md) | the agent harnesses that offer what OATHS needs, with sources and a support level each |
| [BOM.md](BOM.md) | the bill of materials: 28 practices, each with its prior art (a few say where OATHS composes it itself) |
| [example/](example/) | a complete example teammate |
| [IMPLEMENTING.md](IMPLEMENTING.md) | what a reference implementation must show |
| [conformance/](conformance/) | the conformance suite, part 1: identity and provenance, run against this repository's own verifier code (`node conformance/run.mjs`) |
| [tools/](tools/) | the fence check (repository hygiene) |

## Status and roadmap

- **1.0.0 (now):** the five sections, the two formats, the BOM, one example, with the open items marked in each section.
- **Next:** conformance part 2 (state, roles and the session checks, run against an implementation), and the reference implementation linked here.
- **A later release:** a trackback registry, where anyone who implements OATHS can register it, so implementations can find and test against each other.

## Licence

Apache License 2.0, for the specification text and the code alike. See [LICENSE](LICENSE) and [NOTICE](NOTICE). Third-party material and prior art: [CREDITS.md](CREDITS.md). Dependencies: [DEPENDENCIES.md](DEPENDENCIES.md).
