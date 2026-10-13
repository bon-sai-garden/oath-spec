// run.mjs: the OATHS 1.0 conformance suite, part 1 (identity and provenance).
// It generates a throwaway team from example/ with fresh keys, signs and packages it, checks it,
// then plants faults that must each be caught. Nothing it generates is kept.
//     node conformance/run.mjs          exit 0 only when every expectation holds
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { randomBytes } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import * as O from './oaths.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const EXAMPLE = path.join(HERE, '..', 'example', 'eucrates');
const B32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';

function ulid() {
  let t = Date.now(), s = '';
  for (let i = 0; i < 10; i++) { s = B32[t % 32] + s; t = Math.floor(t / 32); }
  for (const b of randomBytes(16)) s += B32[b % 32];
  return s.slice(0, 26);
}
const idOf = (file) => (fs.readFileSync(file, 'utf8').match(/^id:\s*(\S+)$/m) || [])[1] || ulid();

function build() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'oaths-conformance-'));
  fs.cpSync(EXAMPLE, dir, { recursive: true });
  const owner = O.newKey(), other = O.newKey();
  const keys = { [O.fingerprint(owner.publicKey)]: O.rawPublic(owner.publicKey),
                 [O.fingerprint(other.publicKey)]: O.rawPublic(other.publicKey) };
  const files = fs.readdirSync(dir, { recursive: true }).map(String).filter((f) => f.endsWith('.md')).sort();
  for (const rel of files) O.signFile(dir, rel, { signer: 'eucrates', role: 'owner', id: idOf(path.join(dir, rel)), key: owner });
  O.writeManifest(dir, { slug: 'eucrates', owner: 'eucrates', kind: 'teammate', version: '0.1.0',
    build: '0.1.0.1-conformance', source: 'example/eucrates', id: ulid(), key: owner });
  return { dir, keys, owner, other, files };
}

const results = [];
function expect(name, got, want) {
  const ok = want === 'fail' ? got !== 'ok' : got === want;
  results.push(ok);
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : `  (got: ${got})`}${want === 'fail' && ok ? `  [caught: ${got}]` : ''}`);
}
const edit = (p, f) => fs.writeFileSync(p, f(fs.readFileSync(p, 'utf8')));
const editSig = (dir, rel, f) => edit(path.join(dir, rel + '.sig.json'), (s) => JSON.stringify(f(JSON.parse(s)), null, 2));

// ── the good case ────────────────────────────────────────────────────────────────────────────
{
  const t = build();
  for (const rel of t.files) expect(`signature verifies: ${rel}`, O.verifyFile(t.dir, rel, t.keys), 'ok');
  expect('package verifies', O.verifyPackage(t.dir, t.keys), 'ok');
  expect('fingerprint is 32 hex', /^[0-9a-f]{32}$/.test(O.fingerprint(t.owner.publicKey)) ? 'ok' : 'bad', 'ok');
  editSig(t.dir, 'constitution.md', (s) => ({ ...s, _note: 'unsigned, carries no meaning' }));
  expect('a field starting with _ is not signed and changes nothing', O.verifyFile(t.dir, 'constitution.md', t.keys), 'ok');
}

// ── planted faults: each must be caught ─────────────────────────────────────────────────────
const planted = [
  ['a signed file changed by one byte', (t) => { edit(path.join(t.dir, 'constitution.md'), (s) => s + ' '); return O.verifyFile(t.dir, 'constitution.md', t.keys); }],
  ['the target moved to another address', (t) => { editSig(t.dir, 'role.md', (s) => ({ ...s, target: 'elsewhere.md' })); return O.verifyFile(t.dir, 'role.md', t.keys); }],
  ['the timestamp edited after signing', (t) => { editSig(t.dir, 'role.md', (s) => ({ ...s, timestamp: '2000-01-01T00:00:00Z' })); return O.verifyFile(t.dir, 'role.md', t.keys); }],
  ['signed by another key under the owner\'s fingerprint', (t) => {
    const fp = O.fingerprint(t.owner.publicKey);
    O.signFile(t.dir, 'role.md', { signer: 'eucrates', role: 'owner', id: ulid(), key: t.other });
    editSig(t.dir, 'role.md', (s) => ({ ...s, fingerprint: fp }));
    return O.verifyFile(t.dir, 'role.md', t.keys); }],
  ['a signer whose key is not published', (t) => { O.signFile(t.dir, 'role.md', { signer: 'x', role: 'owner', id: ulid(), key: O.newKey() }); return O.verifyFile(t.dir, 'role.md', t.keys); }],
  ['an extra field in the signature', (t) => { editSig(t.dir, 'role.md', (s) => ({ ...s, extra: 'x' })); return O.verifyFile(t.dir, 'role.md', t.keys); }],
  ['a file added to the package', (t) => { fs.writeFileSync(path.join(t.dir, 'smuggled.md'), 'x'); return O.verifyPackage(t.dir, t.keys); }],
  ['a file removed from the package', (t) => { fs.rmSync(path.join(t.dir, 'role.md')); return O.verifyPackage(t.dir, t.keys); }],
  ['the manifest signed as custodian', (t) => {
    const m = JSON.parse(fs.readFileSync(path.join(t.dir, 'MANIFEST.json'), 'utf8'));
    O.signFile(t.dir, 'MANIFEST.json', { signer: m.owner, role: 'custodian', id: ulid(), key: t.owner });
    return O.verifyPackage(t.dir, t.keys); }],
  ['the manifest names a file that is not there', (t) => {
    const p = path.join(t.dir, 'MANIFEST.json'); const m = JSON.parse(fs.readFileSync(p, 'utf8'));
    m.files['eucrates/ghost.md'] = '0'.repeat(64); fs.writeFileSync(p, JSON.stringify(m, null, 2));
    O.signFile(t.dir, 'MANIFEST.json', { signer: m.owner, role: 'owner', id: ulid(), key: t.owner });
    return O.verifyPackage(t.dir, t.keys); }],
];
for (const [name, fault] of planted) { const t = build(); expect(`caught: ${name}`, fault(t), 'fail'); fs.rmSync(t.dir, { recursive: true }); }

const bad = results.filter((r) => !r).length;
console.log(`\n${results.length - bad}/${results.length} expectations hold`);
process.exit(bad ? 1 : 0);
