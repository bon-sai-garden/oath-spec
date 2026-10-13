---
title: Contributing
type: guide
status: active
tags: [oaths, contributing]
---

# Contributing

- **Every practice has a source.** A requirement enters the specification only from a line in [BOM](BOM.md), and a line enters [BOM](BOM.md) only with prior art checked against its primary text. Where OATHS composes known practice into something new, the line says so instead of citing it.
- **Neutral and technical.** No persona, product family or philosophy in the specification; those belong in add-ons.
- **Run the fence before you commit:** `python3 tools/fence-check.py . [--deny <private list>]`.
- **Credit what you use** in [CREDITS](CREDITS.md), with its licence.
- By contributing you agree your contribution is licensed under Apache 2.0.

Write one paragraph, list item or quoted paragraph per line, never hard-wrapped at a column: a hard line break inside a paragraph shows as a false break in some readers. `python3 tools/unwrap-md.py --check .` fails if any file is wrapped, and `python3 tools/unwrap-md.py .` fixes it without changing a word.

A teammate is a colleague, not a thing: write "they" and "their" for a teammate, never "it" or "its".
