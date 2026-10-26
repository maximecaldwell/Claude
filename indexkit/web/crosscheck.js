// Cross-check the browser engine against the Python package.
// Usage: python3 web/make_reference.py ref.json && node web/crosscheck.js ref.json
// Compares, case by case: the list of conventions (names and identical
// readings), the score and hit flag of every convention for the real digits,
// the scores on given paragraph shuffles, and the null-test p-value on
// identical null-draw matrices.
'use strict';
const fs = require('fs');
const IK = require('./engine.js');

const ref = JSON.parse(fs.readFileSync(process.argv[2] || 'ref.json', 'utf8'));
let failures = 0, checked = 0;
function fail(msg) { failures++; if (failures <= 20) console.log('MISMATCH: ' + msg); }

for (const c of ref.cases) {
  const t = IK.Text.fromString(c.text, ref.texts[c.text]);
  const ds = new IK.DigitString(c.digits);
  const cfg = new IK.Config({ mode: c.mode, markers: c.markers });
  const an = new IK.Analysis(t, ds, cfg, ref.targets, ref.wl);
  const id = `${c.text}/${c.mode}/"${c.digits}"`;
  const names = an.convs.map(x => x.name);
  if (JSON.stringify(names) !== JSON.stringify(c.names)) { fail(`${id}: convention lists differ (${names.length} vs ${c.names.length})`); continue; }
  if (JSON.stringify(an.convs.map(x => x.aliases)) !== JSON.stringify(c.aliases)) fail(`${id}: aliases differ`);
  if (an.tv.nMerged !== c.merged) fail(`${id}: merged ${an.tv.nMerged} vs ${c.merged}`);
  const o = an.observed();
  for (let j = 0; j < an.M; j++) {
    if (o.scores[j] !== c.scores[j] || o.hits[j] !== c.hits[j]) { fail(`${id}: ${names[j]} score ${o.scores[j]}/${o.hits[j]} vs ${c.scores[j]}/${c.hits[j]}`); break; }
  }
  if (c.orders) {
    c.orders.forEach((ord, r) => {
      const s = an.evaluate(ds.digits(), Int32Array.from(ord)).scores;
      for (let j = 0; j < an.M; j++) if (s[j] !== c.scoresB[r][j]) { fail(`${id}: shuffle ${r} ${names[j]} ${s[j]} vs ${c.scoresB[r][j]}`); break; }
    });
  }
  checked++;
}

const nt = ref.nulltest, M = nt.obs.length;
const flat = rows => ({ S: Int32Array.from(rows.flat()), N: rows.length });
const n = new IK.NullTest(flat(nt.ref), flat(nt.test), M);
const obs = Int32Array.from(nt.obs);
const p = n.p(obs);
if (p !== nt.p) fail(`null test p ${p} vs ${nt.p}`);
for (let j = 0; j < M; j++) {
  const lr = n.tail.logRarity(obs, j);
  if (Math.abs(lr - nt.lr[j]) > 1e-12) { fail(`log rarity ${j}: ${lr} vs ${nt.lr[j]}`); break; }
}
for (let i = 0; i < nt.stat.length; i++) if (Math.abs(n.nullStat[i] - nt.stat[i]) > 1e-12) { fail(`null stat ${i}`); break; }

console.log(`${checked} cases checked, ${failures} mismatches; null-test p ${p} vs ${nt.p}`);
process.exit(failures ? 1 : 0);
