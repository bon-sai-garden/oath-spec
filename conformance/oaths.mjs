// oaths.mjs: the OATHS 1.0 detached signature and package manifest, as the specification states
// them (spec/provenance.md, spec/identity.md). Node's own crypto only; no dependencies.
import { createHash, generateKeyPairSync, sign as edSign, verify as edVerify, createPublicKey } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

export const FORMAT = 'oaths-sig/1';
export const TAG = 'oaths-sig/1\n';
export const ALGORITHM = 'ed25519+blake2b512';
export const SIG_FIELDS = ['format', 'id', 'signer', 'role', 'fingerprint', 'timestamp', 'algorithm', 'target', 'file-hash', 'signature'];

/** Canonical JSON: keys sorted at every level, no insignificant whitespace, strings as JSON. */
export function canonical(v) {
  if (typeof v === 'string') return JSON.stringify(v);
  if (v && typeof v === 'object' && !Array.isArray(v)) {
    return '{' + Object.keys(v).sort().map((k) => JSON.stringify(k) + ':' + canonical(v[k])).join(',') + '}';
  }
  throw new TypeError('signature fields are strings or objects of strings');
}

export function payload(sig) {
  const rest = {};
  for (const k of Object.keys(sig)) if (k !== 'signature' && !k.startsWith('_')) rest[k] = sig[k];
  return Buffer.from(TAG + canonical(rest), 'utf8');
}

/** The raw 32-byte Ed25519 public key of a KeyObject. */
export function rawPublic(publicKey) {
  const der = publicKey.export({ type: 'spki', format: 'der' });
  return der.subarray(der.length - 32);
}

/** Identity: the first 32 hex characters of SHA-256 over the raw public key. */
export function fingerprint(publicKey) {
  return createHash('sha256').update(rawPublic(publicKey)).digest('hex').slice(0, 32);
}

export function newKey() {
  return generateKeyPairSync('ed25519');
}

export function publicFromRaw(raw) {
  const prefix = Buffer.from('302a300506032b6570032100', 'hex');
  return createPublicKey({ key: Buffer.concat([prefix, raw]), format: 'der', type: 'spki' });
}

const hex = (buf, alg) => createHash(alg).update(buf).digest('hex');

/** Sign `file` (relative to `root`) as `signer`; writes `<file>.sig.json` and returns it. */
export function signFile(root, rel, { signer, role, id, key, timestamp }) {
  const bytes = fs.readFileSync(path.join(root, rel));
  const sig = {
    format: FORMAT, id, signer, role,
    fingerprint: fingerprint(key.publicKey),
    timestamp: timestamp || new Date().toISOString().replace(/\.\d{3}Z$/, 'Z'),
    algorithm: ALGORITHM, target: rel.split(path.sep).join('/'),
    'file-hash': hex(bytes, 'blake2b512'),
  };
  sig.signature = edSign(null, payload(sig), key.privateKey).toString('base64');
  fs.writeFileSync(path.join(root, rel + '.sig.json'), JSON.stringify(sig, null, 2) + '\n');
  return sig;
}

/** Verify `<file>.sig.json`. `keys` maps fingerprint → raw public key (the published keys).
 *  Returns 'ok' or the reason it fails. */
export function verifyFile(root, rel, keys) {
  const sp = path.join(root, rel + '.sig.json');
  if (!fs.existsSync(sp)) return 'no signature';
  let sig;
  try { sig = JSON.parse(fs.readFileSync(sp, 'utf8')); } catch { return 'unreadable signature'; }
  const names = Object.keys(sig).filter((k) => !k.startsWith('_')).sort();
  if (names.join() !== [...SIG_FIELDS].sort().join()) return 'wrong fields';
  if (sig.format !== FORMAT || sig.algorithm !== ALGORITHM) return 'wrong format';
  if (!['owner', 'custodian'].includes(sig.role)) return 'bad role';
  if (sig.target !== rel.split(path.sep).join('/')) return 'target mismatch';
  const raw = keys[sig.fingerprint];
  if (!raw) return 'unknown signer';
  const pub = publicFromRaw(raw);
  if (fingerprint(pub) !== sig.fingerprint) return 'fingerprint mismatch';
  if (!edVerify(null, payload(sig), pub, Buffer.from(sig.signature, 'base64'))) return 'bad signature';
  if (hex(fs.readFileSync(path.join(root, rel)), 'blake2b512') !== sig['file-hash']) return 'hash mismatch';
  return 'ok';
}

function walk(dir, base = dir) {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...walk(p, base));
    else out.push(path.relative(base, p).split(path.sep).join('/'));
  }
  return out.sort();
}

const isManifest = (rel) => rel === 'MANIFEST.json' || rel === 'MANIFEST.json.sig.json';

/** Write MANIFEST.json for the package at `dir` and sign it as its owner. */
export function writeManifest(dir, { slug, owner, kind, version, build, source, id, key }) {
  const files = {};
  for (const rel of walk(dir)) if (!isManifest(rel)) files[`${slug}/${rel}`] = hex(fs.readFileSync(path.join(dir, rel)), 'sha256');
  const m = { slug, owner, kind, version, build, source, algorithm: 'sha256', files };
  fs.writeFileSync(path.join(dir, 'MANIFEST.json'), canonicalPretty(m));
  return signFile(dir, 'MANIFEST.json', { signer: owner, role: 'owner', id, key });
}

function canonicalPretty(m) {
  const sorted = (v) => (v && typeof v === 'object' && !Array.isArray(v))
    ? Object.fromEntries(Object.keys(v).sort().map((k) => [k, sorted(v[k])])) : v;
  return JSON.stringify(sorted(m), null, 2) + '\n';
}

/** Verify a package: the manifest's owner signature first, then every file against it. */
export function verifyPackage(dir, keys) {
  const v = verifyFile(dir, 'MANIFEST.json', keys);
  if (v !== 'ok') return `manifest: ${v}`;
  const m = JSON.parse(fs.readFileSync(path.join(dir, 'MANIFEST.json'), 'utf8'));
  const sig = JSON.parse(fs.readFileSync(path.join(dir, 'MANIFEST.json.sig.json'), 'utf8'));
  if (sig.role !== 'owner' || sig.signer !== m.owner) return 'manifest: not signed by its owner';
  const named = new Set(Object.keys(m.files));
  for (const rel of walk(dir)) {
    if (isManifest(rel)) continue;
    const k = `${m.slug}/${rel}`;
    if (!named.has(k)) return `not in the manifest: ${rel}`;
    if (hex(fs.readFileSync(path.join(dir, rel)), 'sha256') !== m.files[k]) return `changed: ${rel}`;
    named.delete(k);
  }
  if (named.size) return `missing: ${[...named][0]}`;
  return 'ok';
}
