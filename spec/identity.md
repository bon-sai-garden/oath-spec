---
title: Identity
type: spec
version: 1.0.0
status: active
tags: [oaths, spec, identity]
---

# Identity

> [!note] Version 1.0.0
> Every requirement names its bill-of-materials line ([BOM](../BOM.md)); where OATHS composes a practice itself, that line says so. What is still open is marked Open.

> [!info] Key words
> The key words MUST, MUST NOT, SHOULD, SHOULD NOT, RECOMMENDED and MAY are to be read as in BCP 14 (RFC 2119, RFC 8174). Each requirement names the bill-of-materials line it comes from, as [BOM n].

Every teammate can be told apart from every other, by a stranger, without trusting the host that runs them.

1. A teammate MUST hold their own asymmetric signing keypair; Ed25519 is the only algorithm in this version. [BOM 1](../BOM.md#bom-1)
2. A teammate's private key SHOULD be derived on use from a master secret held in custody (HKDF), or held in a signing service or hardware key store, rather than stored one key per teammate on disk. [BOM 2](../BOM.md#bom-2), [BOM 10](../BOM.md#bom-10)
3. A teammate MUST be named by a fingerprint of their public key, computed by a stated hash over the key's encoding. [BOM 3](../BOM.md#bom-3)
4. A teammate's public key MUST be published at a well-known address, or answerable by a published verification endpoint, that anyone can query to check a fingerprint. An endpoint answers for the fingerprint it is asked about; it need not publish a list of keys. [BOM 4](../BOM.md#bom-4)
5. An implementation MAY show a fingerprint visually for humans; a visual form never replaces the comparison of the full fingerprint. [BOM 5](../BOM.md#bom-5)

**Fingerprint.** The first 32 hexadecimal characters of SHA-256 over the raw 32-byte Ed25519 public key, lowercase. A short form (the first 8) MAY be shown to people; it MUST NOT be used to verify.

> [!question] Open
> the shape of the published key document. Direction, not yet normative: a small JSON file at a well-known address listing, per teammate, the name, algorithm, public key, 32-hex fingerprint, created date and a revoked flag. The verification endpoint's question and answer are not specified either; the reference implementation answers one fingerprint per request, checks a signature sent with its payload, and publishes no list. An endpoint that checks a signature for the asker asks to be trusted; how its own answers are checked (for example, signed under a key the asker already holds) is open.
