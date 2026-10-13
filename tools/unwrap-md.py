#!/usr/bin/env python3
"""Unwrap hard-wrapped Markdown: one paragraph, list item or quoted paragraph per line.

    python3 tools/unwrap-md.py [--check] <file-or-dir> ...

Leaves frontmatter, fenced code, tables, headings, rules, html and block ids alone. Refuses to
write a file whose words changed. With --check, changes nothing and exits 1 if any file would change.
"""
import re, sys
from pathlib import Path

LIST = re.compile(r'^(\s*)([-*+]|\d+[.)])\s+')
def is_block(t):
    s = t.strip()
    return (not s or s.startswith(('#', '|', '<', '![', '```', '---', '***', '___')) or re.fullmatch(r'\^[\w-]+', s) is not None)

def unwrap_lines(lines):
    out, i, n = [], 0, len(lines)
    if lines and lines[0].strip() == '---':
        j = next((k for k in range(1, n) if lines[k].strip() == '---'), None)
        if j is not None:
            out += lines[:j + 1]; i = j + 1
    fence = False
    while i < n:
        ln = lines[i]
        if ln.lstrip().startswith('```'):
            fence = not fence; out.append(ln); i += 1; continue
        if fence or is_block(ln):
            out.append(ln); i += 1; continue
        m = re.match(r'^(>\s?)+', ln)
        prefix = m.group(0) if m else ''
        body = ln[len(prefix):]
        lm = LIST.match(body)
        cur = ln.rstrip()
        i += 1
        # quoted callout title or quoted structural line: never join onto it
        if prefix and (body.lstrip().startswith(('[!', '#', '|', '```')) or not body.strip()):
            out.append(ln); continue
        while i < n:
            nx = lines[i]
            nm = re.match(r'^(>\s?)+', nx)
            np_ = nm.group(0) if nm else ''
            nb = nx[len(np_):]
            if np_.replace(' ', '') != prefix.replace(' ', ''): break
            if is_block(nb) or not nb.strip(): break
            if nb.lstrip().startswith(('[!', '```')) or LIST.match(nb): break
            if re.match(r'^\s*\d+[.)]\s', nb): break
            if lm is None and nb.startswith('    ') : break
            cur = cur + ' ' + nb.strip(); i += 1
        out.append(cur)
    return out

def words(text):
    return [w for w in re.split(r'\s+', text) if w and set(w) != {'>'}]

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    check = '--check' in sys.argv
    files = []
    for a in args:
        p = Path(a)
        files += sorted(p.rglob('*.md')) if p.is_dir() else [p]
    changed = 0
    for f in files:
        if '.git' in f.parts or '.obsidian' in f.parts: continue
        old = f.read_text(encoding='utf-8')
        new = '\n'.join(unwrap_lines(old.split('\n')))
        if new == old: continue
        if words(new) != words(old):
            print('REFUSED (words changed):', f); sys.exit(2)
        changed += 1
        print(('would change ' if check else 'unwrapped ') + str(f))
        if not check: f.write_text(new, encoding='utf-8')
    sys.exit(1 if (check and changed) else 0)
main()
