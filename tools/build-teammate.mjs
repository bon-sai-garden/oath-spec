// build-teammate.mjs: package an OATHS teammate folder as a signed, self-checking package.
//     node tools/build-teammate.mjs <teammate-dir> <out-dir> [--force]
// Adds scripts/verify.mjs (with the reference verifier beside it) and identity/keys.json, signs every
// .md and .mjs file with a FRESH key, writes the signed manifest, then verifies the result.
// The key is throwaway and its private half is discarded: the package proves the mechanism works
// (a changed byte is caught); it is not a trust anchor, because it carries its own public key.
import fs from 'node:fs';
import path from 'node:path';
import { randomBytes } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import * as O from '../conformance/oaths.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const B32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
function ulid() {
  let t = Date.now(), s = '';
  for (let i = 0; i < 10; i++) { s = B32[t % 32] + s; t = Math.floor(t / 32); }
  for (const b of randomBytes(16)) s += B32[b % 32];
  return s.slice(0, 26);
}
const idOf = (file) => (fs.readFileSync(file, 'utf8').match(/^id:\s*(\S+)$/m) || [])[1] || ulid();

const [src, out] = process.argv.slice(2).filter((a) => !a.startsWith('--'));
if (!src || !out) { console.error('usage: build-teammate.mjs <teammate-dir> <out-dir> [--force]'); process.exit(2); }
if (fs.existsSync(out)) {
  if (!process.argv.includes('--force')) { console.error(`${out} exists (use --force to replace it)`); process.exit(2); }
  fs.rmSync(out, { recursive: true });
}
fs.cpSync(src, out, { recursive: true });
const slug = path.basename(path.resolve(src));

fs.mkdirSync(path.join(out, 'scripts'), { recursive: true });
fs.copyFileSync(path.join(HERE, '..', 'conformance', 'oaths.mjs'), path.join(out, 'scripts', 'oaths.mjs'));
fs.writeFileSync(path.join(out, 'scripts', 'verify.mjs'), `// verify.mjs: OATHS Conformance 1. Prints 'ok' or the reason; exit 0 only on ok.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { verifyPackage } from './oaths.mjs';
const dir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const published = JSON.parse(fs.readFileSync(path.join(dir, 'identity', 'keys.json'), 'utf8'));
const keys = Object.fromEntries(Object.entries(published).map(([fp, b64]) => [fp, Buffer.from(b64, 'base64')]));
const r = verifyPackage(dir, keys);
console.log(r === 'ok' ? 'ok · signed by ' + Object.keys(keys).map((f) => f.slice(0, 8)).join(', ') : r);
process.exit(r === 'ok' ? 0 : 1);
`);

const key = O.newKey();
fs.mkdirSync(path.join(out, 'identity'), { recursive: true });
fs.writeFileSync(path.join(out, 'identity', 'keys.json'),
  JSON.stringify({ [O.fingerprint(key.publicKey)]: O.rawPublic(key.publicKey).toString('base64') }, null, 2) + '\n');

const files = fs.readdirSync(out, { recursive: true }).map(String)
  .filter((f) => f.endsWith('.md') || f.endsWith('.mjs')).sort();
for (const rel of files) O.signFile(out, rel, { signer: slug, role: 'owner', id: idOf(path.join(out, rel)), key });
O.writeManifest(out, { slug, owner: slug, kind: 'teammate', version: '0.1.0',
  build: '0.1.0.1-' + new Date().toISOString().slice(0, 10).replace(/-/g, ''), source: 'example/' + slug, id: ulid(), key });

const r = O.verifyPackage(out, { [O.fingerprint(key.publicKey)]: O.rawPublic(key.publicKey) });
console.log(`${out}: ${r} · fingerprint ${O.fingerprint(key.publicKey)} · ${files.length} signed files`);
process.exit(r === 'ok' ? 0 : 1);
