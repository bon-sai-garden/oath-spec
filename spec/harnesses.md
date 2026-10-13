---
title: Harnesses
type: spec
version: 1.0.0
status: active
tags: [oaths, spec, harnesses]
---

# Harnesses

> [!info] Checked on 2026-09-29
> Each provider's own documentation was checked. Harness features change quickly; each row names its source, and each level names its evidence.

## Support levels

A harness's support for OATHS is stated at one of four levels. Each level includes the ones before it, and each names its evidence and its date.

- **1 · documented**
  - Means: The vendor's own documentation shows the three mechanisms of the least common denominator: an instruction file, Agent Skills and an MCP client.
  - Evidence: the vendor's documentation, dated
- **2 · verified**
  - Means: A person has loaded the example teammate on the harness and confirmed each of the three mechanisms works.
  - Evidence: a dated record: harness and version, what was checked, by whom
- **3 · tested**
  - Means: The conformance suite passes against an OATHS implementation running on the harness. (Part 1 of the suite today runs against this repository's own verifier code; no third-party implementation can be tested with it yet.)
  - Evidence: the suite's published output: version and date
- **4 · vendor-certified**
  - Means: The vendor itself states that the harness supports OATHS, for example by registering in the trackback registry (a later release).
  - Evidence: the vendor's own statement

> [!important] Nothing is ever claimed above its evidence
> A level that has lapsed (a harness changed, and nobody has re-checked it) drops back to the highest level still evidenced.

## The harnesses

### Claude Code

- **Provider:** Anthropic
- **Instruction file:** `CLAUDE.md`; reads `AGENTS.md` natively
- **Agent Skills:** `.claude/skills/<name>/SKILL.md`
- **MCP client:** yes
- **Level:** 1 · documented

### Claude apps

- **Provider:** Anthropic
- **Instruction file:** project instructions
- **Agent Skills:** skills (need code execution)
- **MCP client:** remote MCP connectors; local MCP on desktop
- **Level:** 1 · documented

### Codex

- **Provider:** OpenAI
- **Instruction file:** `AGENTS.md`
- **Agent Skills:** `.agents/skills/…/SKILL.md`
- **MCP client:** yes
- **Level:** 1 · documented

### ChatGPT

- **Provider:** OpenAI
- **Instruction file:** project instructions
- **Agent Skills:** skills
- **MCP client:** remote MCP through plugins
- **Level:** 1 · documented

### Gemini CLI

- **Provider:** Google
- **Instruction file:** `GEMINI.md`; `AGENTS.md` if configured
- **Agent Skills:** `SKILL.md`
- **MCP client:** yes
- **Level:** 1 · documented

### Grok Build

- **Provider:** xAI
- **Instruction file:** `AGENTS.md`
- **Agent Skills:** `.grok/skills/`
- **MCP client:** yes
- **Level:** 1 · documented

### Mistral Vibe

- **Provider:** Mistral AI
- **Instruction file:** `AGENTS.md`
- **Agent Skills:** `.vibe/skills/`
- **MCP client:** yes
- **Level:** 1 · documented

### Gemini Code Assist (agent mode)

- **Provider:** Google
- **Instruction file:** context files (names unconfirmed)
- **Agent Skills:** not documented
- **MCP client:** yes
- **Level:** below 1: not shown

### OpenClaw

- **Provider:** OpenClaw (open source)
- **Instruction file:** `AGENTS.md` in the workspace, loaded at the start of every session (docs.openclaw.ai/concepts/agent-workspace)
- **Agent Skills:** `SKILL.md` folders, several load locations (docs.openclaw.ai/tools/skills)
- **MCP client:** yes (docs.openclaw.ai/tools/mcp)
- **Level:** 1 · documented

## Sources

- Anthropic: code.claude.com/docs/en/memory, /skills, /sub-agents, /mcp, /hooks, /plugins/overview; support.claude.com (skills, plugins, memory, custom connectors).
- OpenAI: learn.chatgpt.com/docs (agents-md, subagents, build-skills, build-plugins, extend/mcp, hooks, memories, projects).
- Google: geminicli.com/docs (gemini-md, skills, subagents, mcp-server, hooks, auto-memory, extensions); docs.cloud.google.com/gemini/docs/codeassist/agent-mode.
- xAI: docs.x.ai/build (overview, skills-plugins-marketplaces, subagents, hooks, project-rules, mcp-servers).
- Mistral AI: github.com/mistralai/mistral-vibe.
- OpenClaw: docs.openclaw.ai (concepts/agent-workspace, tools/skills, tools/mcp); checked 2026-09-29.
- Conventions: agents.md (Agentic AI Foundation, Linux Foundation); agentskills.io (developed openly at github.com/agentskills/agentskills).

## Add-ons worth writing first

An integrity check (Conformance 1) that runs before the teammate's first action, as a pre-tool or first-prompt hook where the harness documents one. No harness checked documents a session-start hook that can block the session, and where hooks state their failure behaviour some fail open on a timeout or crash (Grok documents this; Mistral Vibe offers a strict mode that denies instead), so this is a hook plus a convention, not a guarantee.

## Later

A trackback registry, where an implementation or harness can register that it supports OATHS and link its conformance results.
