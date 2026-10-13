#!/usr/bin/env python3
"""Draw the bill of materials as a tree: spec/bom-tree.svg.

The data below is the one master for the drawing; BOM.md holds the written lines.
Run:  python3 tools/make-bom-tree.py        (writes spec/bom-tree.svg)
"""
from pathlib import Path
from xml.sax.saxutils import escape

KIND = {"std": "Standards body", "vendor": "Vendor", "open": "Open foundation or community",
        "paper": "Published work", "own": "Composed by OATHS"}

# (indent, name, note, ref, [(source, kind), ...])
GROUPS = [
 ("The teammate: a package", "Conformance 6 · BOM 22, 23", [
  (0, "SKILL.md", "entry point, loaded when relevant", "BOM 22", [("Agent Skills · Anthropic", "vendor"), ("SemVer", "open"), ("integrity check inside: ours", "own")]),
  (0, "constitution.md", "who they are", "State 2 · BOM 14", [("Nygard: decision records", "paper"), ("SBAR handoff", "paper"), ("NIST CM-3: change control", "std"), ("GitHub code owners", "open")]),
  (0, "role.md", "what they are for, who answers for them", "Roles 1–5 · BOM 17, 18, 26–28", [("ANSI/NIST role-based access", "std"), ("NIST AC-5", "std"), ("Entra Agent ID · Microsoft", "vendor"), ("OWASP: excessive agency", "open"), ("IETF RFC 7643", "std"), ("circle, membership: ours", "own")]),
  (0, "state/", "continuity between sessions", "State 1–5 · BOM 13–16, 25", [("AGENTS.md · Agentic AI Foundation", "open")]),
  (1, "working-state.md", "what is open", "", []),
  (1, "journal/", "what happened", "", []),
  (1, "handover.md", "what the next session gets: their own only", "BOM 15", [("Saltzer & Schroeder", "paper")]),
  (1, "circle (private)", "whom they act toward alone; never published", "BOM 27", []),
  (0, "<file>.sig.json", "one detached signature per file", "Provenance · BOM 7, 11", [("IETF RFC 9580", "std"), ("minisign", "open"), ("Sigstore", "open"), ("git · DCO · Linux kernel", "open")]),
  (0, "MANIFEST.json", "every file's hash, signed by the owner", "BOM 8, 9", [("in-toto", "paper"), ("JAR · Oracle", "vendor"), ("Debian", "open"), ("SPDX · ISO/IEC", "std"), ("CycloneDX · Ecma", "std")]),
  (0, "CREDITS.md", "third-party material, credited", "BOM 21", [("REUSE · FSFE", "open"), ("SPDX licence list", "std")]),
 ]),
 ("The identity: beside the package", "Identity 1–5", [
  (0, "an Ed25519 key pair", "", "BOM 1", [("IETF RFC 8032", "std")]),
  (0, "derived from a master secret", "", "BOM 2", [("IETF RFC 5869 (HKDF)", "std")]),
  (0, "the private key, in OS custody", "", "BOM 10", [("Apple", "vendor"), ("Microsoft", "vendor"), ("freedesktop.org", "open")]),
  (0, "a fingerprint of the public key", "", "BOM 3", [("IETF RFC 9580, RFC 4716", "std"), ("OpenSSH", "open")]),
  (0, "published, or answered by an endpoint", "", "BOM 4", [("IETF RFC 8615", "std"), ("IETF RFC 6960 (OCSP)", "std"), ("OpenPGP key directory (draft)", "std")]),
  (0, "a visual form, for humans (optional)", "", "BOM 5", [("Perrig & Song", "paper"), ("OpenSSH", "open")]),
 ]),
 ("The harness: runs the teammate", "not specified by OATHS", [
  (0, "instruction file, read at start", "CLAUDE.md · AGENTS.md · GEMINI.md", "BOM 13", [("Anthropic", "vendor"), ("Agentic AI Foundation", "open")]),
  (0, "tools over a standard protocol", "MCP", "BOM 24", [("Anthropic, 2024", "vendor"), ("Agentic AI Foundation", "open")]),
  (0, "integrity checked first, no fallback", "", "BOM 12", [("Saltzer & Schroeder", "paper"), ("UEFI Forum", "std"), ("TCG", "std")]),
  (0, "hooks, sub-agents, built-in memory", "add-ons; they differ per harness", "", []),
 ]),
 ("The discipline: applies to all of it", "Conformance", [
  (0, "documents carry a generated id", "", "BOM 6", [("ULID", "open"), ("IETF RFC 9562", "std")]),
  (0, "a check is trusted once seen to fail", "", "BOM 19", [("Beck: TDD", "paper"), ("DeMillo et al.", "paper")]),
  (0, "one master, copies generated", "", "BOM 20", [("Hunt & Thomas: DRY", "paper"), ("gated on drift: ours", "own")]),
  (0, "the builder is not the verifier", "", "BOM 18", [("NIST AC-5", "std")]),
 ]),
 ("The guards: what a failure leaves behind", "State 5 · BOM 25, 19, 16", [
  (0, "state/lessons.md", "what went wrong, the guard added, seen to fail", "BOM 25, 19", [("Hashimoto: engineer the harness", "paper"), ("Google SRE: postmortems", "paper"), ("Beck · DeMillo (seen to fail)", "paper")]),
  (0, "patterns.md, or the instruction file", "lessons that passed review; a human can veto", "BOM 25, 16", [("AGENTS.md · Agentic AI Foundation", "open"), ("NIST CM-3: change control", "std"), ("GitHub code owners", "open")]),
 ]),
]

W = 1080
COL = {  # light, dark  (fill, stroke, text)
 "std":    (("#e8f0fb", "#7ba3dd", "#1d3f73"), ("#1c2b45", "#4f79b8", "#bcd2f5")),
 "vendor": (("#fbf0dc", "#d3a24d", "#6b4610"), ("#3b2f18", "#a97c2e", "#f1d9a6")),
 "open":   (("#e6f4e8", "#78b585", "#1f5a2c"), ("#1d3524", "#4f8c5d", "#b9e2c2")),
 "paper":  (("#f0e9f8", "#a58ccc", "#4a2f78"), ("#2c2340", "#8067ab", "#d6c7ef")),
 "own":    (("#ececec", "#9a9a9a", "#333333"), ("#333333", "#8a8a8a", "#e6e6e6")),
}

def css():
    out = [".bgr{fill:#ffffff} .fg{fill:#1b1f24} .mu{fill:#5b6470} .ln{stroke:#c5ccd6} .bd{fill:#f4f6f9}",
           "@media (prefers-color-scheme:dark){.bgr{fill:#16191d} .fg{fill:#e6e9ee} .mu{fill:#98a2b0} .ln{stroke:#3a424d} .bd{fill:#1e2329}}",
           "text{font-family:system-ui,-apple-system,'Segoe UI',sans-serif}",
           ".m{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}"]
    for k, (l, d) in COL.items():
        out.append(f".p-{k}{{fill:{l[0]};stroke:{l[1]}}} .t-{k}{{fill:{l[2]}}}")
        out.append(f"@media (prefers-color-scheme:dark){{.p-{k}{{fill:{d[0]};stroke:{d[1]}}} .t-{k}{{fill:{d[2]}}}}}")
    return "\n".join(out)

def build():
    y = 20; parts = []
    parts.append(f'<text x="28" y="{y+14}" font-size="18" font-weight="600" class="fg">The bill of materials as a tree</text>')
    y += 34
    # legend
    x = 28
    for k, label in KIND.items():
        w = len(label) * 6.3 + 28
        parts.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="20" rx="10" class="p-{k}" stroke-width="1"/>'
                     f'<text x="{x+13}" y="{y+14}" font-size="11" class="t-{k}">{escape(label)}</text>')
        x += w + 10
    y += 40
    for title, sect, rows in GROUPS:
        parts.append(f'<rect x="14" y="{y}" width="{W-28}" height="30" rx="6" class="bd"/>'
                     f'<text x="28" y="{y+20}" font-size="14" font-weight="600" class="fg">{escape(title)}</text>'
                     f'<text x="{W-28}" y="{y+20}" font-size="12" text-anchor="end" class="mu">{escape(sect)}</text>')
        y += 40
        top = y - 6
        for ind, name, note, ref, srcs in rows:
            nx = 44 + ind * 24
            h = 44 if srcs else 28
            parts.append(f'<line x1="{nx-14}" y1="{y+9}" x2="{nx-4}" y2="{y+9}" class="ln" stroke-width="1.2"/>')
            mono = "m " if ("." in name or name.endswith("/")) else ""
            t = f'<text x="{nx}" y="{y+13}" font-size="13" font-weight="600" class="{mono}fg">{escape(name)}'
            if note:
                t += f'<tspan font-weight="400" font-family="system-ui,sans-serif" font-size="12" class="mu" dx="10">{escape(note)}</tspan>'
            parts.append(t + '</text>')
            if ref:
                parts.append(f'<text x="{W-28}" y="{y+13}" font-size="12" text-anchor="end" class="mu">{escape(ref)}</text>')
            px = nx
            for s, k in srcs:
                w = len(s) * 6.3 + 22
                parts.append(f'<rect x="{px:.0f}" y="{y+22}" width="{w:.0f}" height="19" rx="9.5" class="p-{k}" stroke-width="1"/>'
                             f'<text x="{px+10:.0f}" y="{y+35.5}" font-size="11" class="t-{k}">{escape(s)}</text>')
                px += w + 6
            y += h + 4
        parts.append(f'<line x1="30" y1="{top}" x2="30" y2="{y-14}" class="ln" stroke-width="1.2"/>')
        y += 12
    y += 4
    parts.append(f'<text x="28" y="{y}" font-size="11" class="mu">Numbers are the lines of the bill of materials (BOM.md); section names are the OATHS sections that specify each practice. Generated by tools/make-bom-tree.py.</text>')
    H = y + 18
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" role="img" '
            f'aria-labelledby="t d"><title id="t">The bill of materials as a tree</title>'
            f'<desc id="d">The parts of an AI teammate (package, identity, harness, discipline), each with its bill-of-materials line and the body its practice comes from.</desc>'
            f'<style>{css()}</style><rect width="{W}" height="{H}" class="bgr"/>' + "".join(parts) + '</svg>\n')

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "spec" / "bom-tree.svg"
    out.write_text(build(), encoding="utf-8")
    print("wrote", out)
