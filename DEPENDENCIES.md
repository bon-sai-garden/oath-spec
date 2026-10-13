---
title: Dependencies
type: reference
status: active
tags: [oaths, dependencies]
---

# Dependencies

OATHS is a specification: nothing is needed to read it.

| Tool | Needs |
|---|---|
| `tools/fence-check.py` | Python 3.10 or later, standard library only; `git` |
| `conformance/` | Node.js 18 or later, its built-in `crypto` only (Ed25519, BLAKE2b-512, SHA-256) |

A conforming implementation brings its own dependencies; see IMPLEMENTING.md.
