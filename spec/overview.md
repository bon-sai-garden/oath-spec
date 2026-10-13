---
title: Overview
type: spec
version: 1.0.0
status: active
tags: [oaths, spec, overview]
---

# Overview

> [!note] Version 1.0.0
> The key words MUST, MUST NOT, SHOULD, SHOULD NOT, RECOMMENDED and MAY are to be read as in BCP 14 (RFC 2119, RFC 8174).

## What OATHS specifies

An **AI teammate** is an agent that a person or a team works with over many sessions. OATHS specifies what such a teammate needs so that their work can be continued, checked and trusted:

- **Identity:** who they are, checkable by a stranger.
- **Provenance:** what they made, and whether that has changed since.
- **State:** what they carry from one session to the next.
- **Roles:** what they are for.
- **Conformance:** the checks that hold the rest true.

## The least common denominator

OATHS asks only for what every capable agent harness already offers: files read at the start of a session, a way to package instructions and resources, and tools over the Model Context Protocol. A teammate that uses only these runs on any of them. The harnesses OATHS targets, and what each already provides, are listed in [harnesses](harnesses.md); the anatomy of a teammate is in [anatomy](anatomy.md).

## Add-ons

An **add-on** layers something specific on top: a harness's own features (its hooks, its sub-agents, its memory), a richer character specification, or a team's own conventions. An add-on:

1. MUST NOT change what an OATHS field means;
2. MUST be optional: a teammate without the add-on stays conformant;
3. SHOULD say which harness or which layer it is for.

## What OATHS is not

Not a model, not a harness and not an agent framework. It doesn't specify a personality, a prompt, or how a model reasons. It specifies the parts around the model that make a teammate continuous and accountable.
