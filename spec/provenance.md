---
title: Provenance
type: spec
version: 1.0.0
status: active
tags: [oaths, spec, provenance]
---

# Provenance

> [!note] Version 1.0.0
> Every requirement names its bill-of-materials line ([BOM](../BOM.md)); where OATHS composes a practice itself, that line says so. What is still open is marked Open.

> [!info] Key words
> The key words MUST, MUST NOT, SHOULD, SHOULD NOT, RECOMMENDED and MAY are to be read as in BCP 14 (RFC 2119, RFC 8174). Each requirement names the bill-of-materials line it comes from, as [BOM n].

Every file a teammate produces can be checked for who made it and whether it has changed.

1. A signed file MUST carry a detached signature beside it; the signature MUST cover the file's exact bytes and name the signer's fingerprint and the file's address. [BOM 7](../BOM.md#bom-7)
2. A package MUST carry a manifest naming every file and its hash, and the manifest MUST be signed by the package's owner. [BOM 8](../BOM.md#bom-8)
3. A package SHOULD declare the third-party materials it contains in a standard form. [BOM 9](../BOM.md#bom-9)
4. Private keys MUST stay in operating-system custody or behind a signing service; they MUST NOT be written to disk in the clear. [BOM 10](../BOM.md#bom-10)
5. A signature claims authorship. A signer who edits a file owned by another MUST NOT sign it as its owner; a signature made in an owner's name MUST be reviewed by that owner before it is committed. [BOM 11](../BOM.md#bom-11)

## Format: the detached signature

Written from an implementation in use, not designed on paper.

A signed file `F` has a sidecar `F.sig.json`: a JSON object with exactly these fields, all strings.

| field | value |
|---|---|
| `format` | `"oaths-sig/1"` |
| `id` | the file's stable identifier (a ULID). A file that carries its own id in a header carries the same one here. |
| `signer` | the signer's name, lowercase letters, digits and hyphens |
| `role` | `"owner"` or `"custodian"`. A custodian signature attests that the file was held, never that it was written. [BOM 11](../BOM.md#bom-11) |
| `fingerprint` | the signer's fingerprint (see Identity) |
| `timestamp` | `YYYY-MM-DDTHH:MM:SSZ`, UTC |
| `algorithm` | `"ed25519+blake2b512"` |
| `target` | the file's path relative to its signing root, `/`-separated |
| `file-hash` | BLAKE2b-512 of the file's exact bytes, lowercase hex |
| `signature` | Ed25519 over the payload below, base64 |

**Payload.** `UTF-8("oaths-sig/1\n" + canonical(every field except signature))`, where `canonical` writes an object with its keys sorted at every level, no insignificant whitespace, and strings escaped as JSON. The leading tag means a signature made for anything else can never verify as this one. Fields whose names begin with `_` are not signed and carry no meaning.

**Signing root.** The nearest directory above the file that is a repository root or carries the implementation's root marker. It is found by the marker, never by counting directory levels; no root found is a refusal. A package carries a root marker, so its files keep package-relative targets wherever it is unpacked.

**Verifying.** Recompute the hash, rebuild the payload, check the signature against the public key published for `fingerprint` (or ask the verification endpoint that answers for it, [Identity 4](identity.md)), and check that `target` is the file's address. Any mismatch fails.

> [!note] The reference implementation's seal file differs, for now
> The implementation this format was written from currently writes a different seal file, and neither verifier yet accepts the other's. The format above is the one OATHS specifies; bringing the two together is open.

## Format: the package manifest

A package carries `MANIFEST.json` at its root, signed by its owner with a detached signature as above.

| field | value |
|---|---|
| `slug` | the package's name |
| `owner` | the owner's name; the manifest's signature MUST be the owner's, `role: "owner"` |
| `kind` | what the package is (for example a teammate, a skill, a bundle of them) |
| `version` | `MAJOR.MINOR.PATCH` [BOM 23](../BOM.md#bom-23) |
| `build` | the build's own stamp |
| `source` | where it was built from: a repository and a commit |
| `algorithm` | `"sha256"` |
| `files` | an object: every shipped file's path (prefixed by `slug/`) → its SHA-256, hex |

`files` names every byte the package ships except `MANIFEST.json` and its own signature. The package's integrity check [BOM 22](../BOM.md#bom-22) recomputes every hash, rejects any file that is missing, changed or not named, and verifies the manifest's signature before anything in the package is used.

> [!question] Open
> - The reference implementation's seal file and the format above are to converge (see the note under the detached signature); which side moves is not decided.
> - Canonical JSON: the key order, the escaping of non-ASCII characters and the handling of arrays are not yet stated byte for byte. The direction is to adopt RFC 8785 (JSON Canonicalization Scheme).
> - The sidecar's "exactly these fields" and the allowed unsigned `_` fields need one sentence to reconcile them.
> - The signing-root marker is not yet named, and the manifest's `slug/` path prefix and a signature's `target` use different path bases.
> - The two hashes (BLAKE2b-512 for a file, SHA-256 in the manifest) have no stated reason, and neither has a line in the bill of materials.
> - A package that carries its own public key has no trust anchor; how a reader gets the key they trust, and how an old but validly signed file is told from a new one, are not yet specified.
> - Fixed test vectors, so a second implementation can be checked byte for byte.
