---
title: Conformance
type: spec
version: 1.0.0
status: active
tags: [oaths, spec, conformance]
---

# Conformance

> [!note] Version 1.0.0
> Every requirement names its bill-of-materials line ([BOM](../BOM.md)); where OATHS composes a practice itself, that line says so. What is still open is marked Open.

> [!info] Key words
> The key words MUST, MUST NOT, SHOULD, SHOULD NOT, RECOMMENDED and MAY are to be read as in BCP 14 (RFC 2119, RFC 8174). Each requirement names the bill-of-materials line it comes from, as [BOM n].

The checks an implementation runs, and how they are allowed to fail.

1. A session MUST check its own integrity before it does anything else. Any result but a pass MUST stop the session; it MUST NOT fall back to an unchecked path. Where a harness cannot block a session at its start, the check MUST run before the teammate's first action (the first prompt handled or the first tool call), by a hook where the harness has one, and otherwise by an instruction in the teammate's instruction file that says to run it first. [BOM 12](../BOM.md#bom-12)
2. Documents SHOULD carry a stable, generated identifier, and references SHOULD use it rather than a path. [BOM 6](../BOM.md#bom-6)
3. A check SHOULD be trusted only once it has been seen to fail. [BOM 19](../BOM.md#bom-19)
4. Each piece of knowledge has one master; any copy is generated from it, and a check fails when the copy has drifted. [BOM 20](../BOM.md#bom-20)
   - For **trust material** (identities, public keys, signatures and manifests) this is a MUST: a stale copy of trust material is a security fault.
   - For everything else (documentation, caches, derived views) it is a SHOULD: an implementation MAY keep an independent copy if it states why.
5. Third-party material MUST be credited in one checked file. [BOM 21](../BOM.md#bom-21)
6. A package MUST be self-contained and carry its own integrity check. [BOM 22](../BOM.md#bom-22) Versions SHOULD follow Semantic Versioning. [BOM 23](../BOM.md#bom-23)
7. Tools SHOULD be exposed to the model over a standard protocol. [BOM 24](../BOM.md#bom-24)

> [!question] Open
> which requirements a minimal implementation may leave out. The conformance suite: part 1 (identity and provenance) exists and runs against this repository's own verifier code, so a third party cannot yet point it at their own implementation; fixed test vectors, and part 2 (state, roles and the session checks), are still to come. The suite checks the seal file exactly as Provenance specifies it, so it does not accept the reference implementation's current seal file (see the note in [Provenance](provenance.md)). Part 2 will check [Roles](roles.md) 3 to 5 only where they apply, so that no check makes a SHOULD or a MAY required: where a sponsor is named, they are not a teammate; where a circle exists, it is in no package and nowhere published; where a cohort exists, a membership recorded on one side only is not a membership. Part 1 does not check them: the role file's fields and the cohort record's shape are not yet normative, and a check would make the suite their specification.
