/* indexkit engine for the browser.
 *
 * A line-by-line port of the Python package (indexkit/*.py).  Same
 * conventions, same scores, same tail model and p-value rule; only the
 * random number generator differs, so p-values agree with the Python tool
 * up to Monte-Carlo noise.  web/crosscheck.js verifies the port against the
 * Python code on the same inputs.
 *
 * Works as a plain <script> (defines self.IndexKit), inside a Web Worker,
 * and under node (module.exports).
 */
(function (root) {
  'use strict';

  var VERSION = '1.0.0-web';
  var MIN_DRAWS = 10000;

  // ------------------------------------------------------------------
  // Text: Unicode clean-up, folding, tokenizers (text.py)
  // ------------------------------------------------------------------

  // Exactly Python's str.isspace() set.
  var WS = '\\t\\n\\v\\f\\r\\x1c-\\x1f \\x85\\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000';
  var RE_WS_TOKEN = new RegExp('[^' + WS + ']+', 'gu');
  var RE_IS_WS = new RegExp('^[' + WS + ']$', 'u');
  var RE_LSTRIP = new RegExp('^[' + WS + ']+', 'u');
  var RE_RSTRIP = new RegExp('[' + WS + ']+$', 'u');
  var RE_ALNUM_RUN = /[\p{L}\p{N}]+/gu;
  var RE_ALNUM = /^[\p{L}\p{N}]$/u;
  var RE_HAS_ALNUM = /[\p{L}\p{N}]/u;
  var RE_ALPHA = /^\p{L}$/u;
  var RE_SENT_END = new RegExp('[.!?\\u2026]+(?:[' + WS + ']*[\\u00bb\\u201d)\\]]|["\'\\u2019])*(?=[' + WS + ']|$)', 'gu');

  function lstrip(s) { return s.replace(RE_LSTRIP, ''); }
  function rstrip(s) { return s.replace(RE_RSTRIP, ''); }
  function strip(s) { return rstrip(lstrip(s)); }

  function normalize(raw) {
    if (raw.charAt(0) === '﻿') raw = raw.slice(1);
    raw = raw.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    return raw.normalize('NFC');
  }

  var LIG = { 'œ': 'oe', 'Œ': 'oe', 'æ': 'ae', 'Æ': 'ae', 'ß': 'ss', 'ẞ': 'ss' };

  function fold(s) {
    var out = '';
    for (var ch0 of s.normalize('NFKD')) {
      var ch = LIG[ch0] || ch0;
      var low = ch.toLowerCase();
      for (var c of low) if (c >= 'a' && c <= 'z') out += c;
    }
    return out;
  }

  function letterCode(s) {
    var f = fold(s);
    return f ? f.charCodeAt(0) - 97 : -1;
  }

  var TOKENIZERS = ['ws', 'ws-drop', 'strip', 'split'];
  var TOKENIZER_HELP = {
    'ws': "split on whitespace only; standalone punctuation such as ':' '–' '«' counts as a word",
    'ws-drop': 'split on whitespace, then drop tokens that contain no letter or digit',
    'strip': 'split on whitespace, strip punctuation from both ends of each token, drop empty ones',
    'split': "split on whitespace, hyphens and apostrophes too (Val-d'Or -> Val d Or, l'Or -> l Or)"
  };

  function hasAlnum(s) { return RE_HAS_ALNUM.test(s); }

  function tokenize(s, name) {
    var out = [], m;
    if (name === 'split') {
      RE_ALNUM_RUN.lastIndex = 0;
      while ((m = RE_ALNUM_RUN.exec(s)) !== null) out.push([m[0], m.index, m.index + m[0].length]);
      return out;
    }
    var raw = [];
    RE_WS_TOKEN.lastIndex = 0;
    while ((m = RE_WS_TOKEN.exec(s)) !== null) raw.push([m[0], m.index, m.index + m[0].length]);
    if (name === 'ws') return raw;
    if (name === 'ws-drop') return raw.filter(function (t) { return hasAlnum(t[0]); });
    if (name === 'strip') {
      for (var k = 0; k < raw.length; k++) {
        var tok = raw[k][0], a = raw[k][1];
        var cps = Array.from(tok);
        var i = 0, j = cps.length;
        while (i < j && !RE_ALNUM.test(cps[i])) i++;
        while (j > i && !RE_ALNUM.test(cps[j - 1])) j--;
        if (i < j) {
          var pre = cps.slice(0, i).join('').length;
          var body = cps.slice(i, j).join('');
          out.push([body, a + pre, a + pre + body.length]);
        }
      }
      return out;
    }
    throw new Error('unknown tokenizer ' + name);
  }

  function tokens(s, name) { return tokenize(normalize(s), name).map(function (t) { return t[0]; }); }

  function lineSpans(p) {
    var out = [], pos = 0, lines = p.split('\n');
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      var a = pos + (line.length - lstrip(line).length);
      var b = pos + rstrip(line).length;
      if (b > a) out.push([p.slice(a, b), a, b]);
      pos += line.length + 1;
    }
    return out;
  }

  function sentenceSpans(p) {
    var out = [], start = 0, ends = [], m;
    RE_SENT_END.lastIndex = 0;
    while ((m = RE_SENT_END.exec(p)) !== null) {
      ends.push(m.index + m[0].length);
      if (m[0].length === 0) RE_SENT_END.lastIndex++;
    }
    if (!ends.length || ends[ends.length - 1] < p.length) ends.push(p.length);
    for (var i = 0; i < ends.length; i++) {
      var end = ends[i], seg = p.slice(start, end);
      var a = start + (seg.length - lstrip(seg).length);
      var b = start + rstrip(seg).length;
      if (b > a && hasAlnum(p.slice(a, b))) out.push([p.slice(a, b), a, b]);
      start = end;
    }
    return out;
  }

  function Text(label, paragraphs, path, sha) {
    if (!paragraphs.length) throw new Error('text ' + label + ' is empty');
    this.label = label;
    this.paragraphs = paragraphs;
    this.path = path || '(pasted)';
    this.sha256 = sha || sha256Hex(utf8(paragraphs.join('\n\n')));
  }
  Text.fromString = function (label, raw, path, sha) {
    var text = normalize(raw);
    var lines = text.split('\n');
    var i = 0;
    while (i < lines.length && !strip(lines[i])) i++;
    if (i === lines.length) throw new Error('The ' + label + ' text is empty.');
    var paragraphs = [strip(lines[i])], current = [];
    for (var k = i + 1; k < lines.length; k++) {
      var line = lines[k];
      if (strip(line)) current.push(rstrip(line));
      else if (current.length) { paragraphs.push(current.join('\n')); current = []; }
    }
    if (current.length) paragraphs.push(current.join('\n'));
    return new Text(label, paragraphs, path, sha);
  };
  Text.prototype.wordCount = function () {
    var n = 0;
    for (var i = 0; i < this.paragraphs.length; i++) n += tokenize(this.paragraphs[i], 'ws-drop').length;
    return n;
  };
  Text.prototype.findMarker = function (marker) {
    var alts = normalize(marker).split('|').map(strip).filter(Boolean);
    for (var ai = 0; ai < alts.length; ai++) {
      var needle = alts[ai].toLowerCase();
      for (var pi = 0; pi < this.paragraphs.length; pi++) {
        var ls = lineSpans(this.paragraphs[pi]);
        for (var li = 0; li < ls.length; li++) {
          if (ls[li][0].toLowerCase().indexOf(needle) >= 0) return [pi, ls[li][1], alts[ai]];
        }
      }
    }
    return null;
  };

  // ------------------------------------------------------------------
  // Random numbers (seeded; xoshiro128**)
  // ------------------------------------------------------------------

  function splitmix32(a) {
    return function () {
      a = (a + 0x9e3779b9) | 0;
      var t = a ^ (a >>> 16);
      t = Math.imul(t, 0x21f0aaad);
      t = t ^ (t >>> 15);
      t = Math.imul(t, 0x735a2d97);
      return (t ^ (t >>> 15)) >>> 0;
    };
  }

  function makeRng(parts) {
    var h = 0x811c9dc5;
    for (var i = 0; i < parts.length; i++) {
      var v = parts[i] >>> 0;
      for (var k = 0; k < 4; k++) { h ^= (v >>> (8 * k)) & 255; h = Math.imul(h, 0x01000193); }
      h ^= Math.floor(parts[i] / 4294967296) | 0;
      h = Math.imul(h, 0x01000193);
    }
    var sm = splitmix32(h);
    var s0 = sm(), s1 = sm(), s2 = sm(), s3 = sm();
    function next() {
      var r = Math.imul(s1, 5);
      r = Math.imul((r << 7) | (r >>> 25), 9) >>> 0;
      var t = s1 << 9;
      s2 ^= s0; s3 ^= s1; s1 ^= s2; s0 ^= s3; s2 ^= t;
      s3 = (s3 << 11) | (s3 >>> 21);
      return r;
    }
    return {
      random: function () { return next() / 4294967296; },
      int: function (n) { return Math.floor(next() / 4294967296 * n); }
    };
  }

  // ------------------------------------------------------------------
  // Digits (digits.py)
  // ------------------------------------------------------------------

  var GROUPINGS = ['given', 'single', 'pairs', 'cumulative', 'reversed'];
  var GROUPING_HELP = {
    'given': 'numbers exactly as grouped in the string (no separators = one big number)',
    'single': 'every digit on its own',
    'pairs': 'digits taken two at a time, ignoring the separators (an odd last digit stays single)',
    'cumulative': 'the given numbers are steps: each position = previous position + next number',
    'reversed': 'the whole string read backwards, then grouped as given'
  };
  var MAX_DIGITS = 60, MAX_GROUP = 15;

  function DigitString(raw) {
    this.raw = strip(raw);
    this.groups = this.raw.match(/[0-9]+/g) || [];
    this.seps = this.raw.split(/[0-9]+/);
    if (!this.groups.length) throw new Error('No digits found in "' + raw + '".');
    this.lengths = this.groups.map(function (g) { return g.length; });
    this.nDigits = this.lengths.reduce(function (a, b) { return a + b; }, 0);
    if (this.nDigits > MAX_DIGITS) throw new Error('At most ' + MAX_DIGITS + ' digits are supported.');
    if (Math.max.apply(null, this.lengths) > MAX_GROUP) throw new Error('A single group may have at most ' + MAX_GROUP + ' digits.');
  }
  DigitString.prototype.shape = function () { return this.lengths.join('-'); };
  DigitString.prototype.digits = function () { return Array.from(this.groups.join('')).map(Number); };
  DigitString.prototype.randomDigits = function (rng, out) {
    for (var i = 0; i < this.nDigits; i++) out[i] = rng.int(10);
    return out;
  };

  function givenNums(d, lengths, out) {
    var pos = 0;
    for (var g = 0; g < lengths.length; g++) {
      var v = 0;
      for (var i = 0; i < lengths[g]; i++) v = v * 10 + d[pos + i];
      out.push(v);
      pos += lengths[g];
    }
    return out;
  }

  function numbers(grouping, d, lengths) {
    var n = d.length, i, out;
    if (grouping === 'given') return givenNums(d, lengths, []);
    if (grouping === 'single') return Array.prototype.slice.call(d, 0, n);
    if (grouping === 'pairs') {
      var L = [];
      for (i = 0; i < Math.floor(n / 2); i++) L.push(2);
      if (n % 2) L.push(1);
      return givenNums(d, L, []);
    }
    if (grouping === 'cumulative') {
      out = givenNums(d, lengths, []);
      for (i = 1; i < out.length; i++) out[i] += out[i - 1];
      return out;
    }
    if (grouping === 'reversed') {
      var r = [];
      for (i = n - 1; i >= 0; i--) r.push(d[i]);
      return givenNums(r, lengths.slice().reverse(), []);
    }
    throw new Error('unknown grouping ' + grouping);
  }

  function distinctGroupings(ds, groupings) {
    var rng = makeRng([0, 7]);
    var probes = [ds.digits()];
    for (var k = 0; k < 50; k++) probes.push(ds.randomDigits(rng, new Array(ds.nDigits)));
    var kept = [], outs = [];
    groupings.forEach(function (g) {
      var out = probes.map(function (p) { return numbers(g, p, ds.lengths).join(','); }).join(';');
      var idx = outs.indexOf(out);
      if (idx >= 0) kept[idx].push(g);
      else { kept.push([g]); outs.push(out); }
    });
    return kept;
  }

  // ------------------------------------------------------------------
  // Conventions (conventions.py)
  // ------------------------------------------------------------------

  var UNITS = ['word', 'letter', 'nonspace', 'line', 'sentence', 'paragraph'];
  var UNIT_HELP = {
    'word': 'the n-th word (depends on the tokenizer)',
    'letter': 'the n-th letter (a-z and accented letters; spaces, digits, punctuation skipped)',
    'nonspace': 'the n-th character that is not a space (punctuation and digits count)',
    'line': 'the n-th non-empty line of the file',
    'sentence': 'the n-th sentence',
    'paragraph': 'the n-th paragraph (the title is paragraph 1 when counting from the title)'
  };
  var READS = {
    word: ['item', 'initial'], letter: ['char'], nonspace: ['char'],
    line: ['item', 'initial'], sentence: ['item', 'initial'], paragraph: ['item', 'initial']
  };
  var BASES = [0, 1];
  var DEFAULT_STARTS = ['title', 'body'];

  function ordered(allowed, given) { return allowed.filter(function (x) { return given.indexOf(x) >= 0; }); }

  function Config(o) {
    o = o || {};
    if (o.mode !== 'targets' && o.mode !== 'letters') throw new Error("score must be 'targets' or 'letters'");
    var chk = function (name, given, allowed, mayBeEmpty) {
      var bad = given.filter(function (g) { return allowed.indexOf(g) < 0; });
      if (bad.length || (!given.length && !mayBeEmpty)) throw new Error('Bad ' + name + ' list: ' + given.join(','));
    };
    var units = o.units || UNITS, toks = o.tokenizers || TOKENIZERS, bases = o.bases || BASES;
    var starts = o.starts || DEFAULT_STARTS, groupings = o.groupings || GROUPINGS, markers = o.markers || [];
    chk('unit', units, UNITS); chk('tokenizer', toks, TOKENIZERS); chk('base', bases, BASES);
    chk('start', starts, DEFAULT_STARTS, true); chk('grouping', groupings, GROUPINGS);
    if (!starts.length && !markers.length) throw new Error('Need at least one start point.');
    this.mode = o.mode;
    this.units = ordered(UNITS, units);
    this.tokenizers = ordered(TOKENIZERS, toks);
    this.bases = ordered(BASES, bases);
    this.starts = ordered(DEFAULT_STARTS, starts);
    this.markers = markers.slice();
    this.groupings = ordered(GROUPINGS, groupings);
  }
  Config.prototype.isRestricted = function () {
    return this.units.length !== UNITS.length || this.tokenizers.length !== TOKENIZERS.length ||
      this.bases.length !== BASES.length || this.starts.length !== DEFAULT_STARTS.length ||
      this.groupings.length !== GROUPINGS.length;
  };
  Config.prototype.toDict = function () {
    return { score: this.mode, units: this.units, tokenizers: this.tokenizers, bases: this.bases,
      starts: this.starts, markers: this.markers, groupings: this.groupings };
  };
  Config.fromDict = function (d) {
    return new Config({ mode: d.score, units: d.units, tokenizers: d.tokenizers, bases: d.bases,
      starts: d.starts, markers: d.markers, groupings: d.groupings });
  };

  function View(name, kind, paraCodes, paraDisp, start) {
    this.name = name;
    this.aliases = [name];
    this.kind = kind;
    var P = paraCodes.length;
    this.paraLen = new Int32Array(P);
    this.paraBase = new Int32Array(P);
    var total = 0;
    for (var i = 0; i < P; i++) { this.paraBase[i] = total; this.paraLen[i] = paraCodes[i].length; total += paraCodes[i].length; }
    this.flat = new Int32Array(total);
    for (i = 0; i < P; i++) this.flat.set(paraCodes[i], this.paraBase[i]);
    this.disp = [].concat.apply([], paraDisp);
    this.start = start;
    this.startFlat = start[0] === 'slot' ? this.paraBase[start[1]] : this.paraBase[start[1]] + start[2];
    this.signature = kind + '|' + start.join(',') + '|' + paraCodes.map(function (c) { return Array.prototype.join.call(c, ','); }).join(';');
  }

  function unitItems(p, unit, tok) {
    var out = [], i = 0;
    if (unit === 'word') return tokenize(p, tok).map(function (t) { return [t[0], t[0], t[1], t[2]]; });
    if (unit === 'letter' || unit === 'nonspace') {
      for (var c of p) {
        var keep = unit === 'letter' ? RE_ALPHA.test(c) : !RE_IS_WS.test(c);
        if (keep) out.push([c, c, i, i + c.length]);
        i += c.length;
      }
      return out;
    }
    var spans = unit === 'line' ? lineSpans(p) : unit === 'sentence' ? sentenceSpans(p) : [[p, 0, p.length]];
    return spans.map(function (s) {
      var first = tokenize(s[0], 'strip');
      var w = first.length ? first[0][0] : '';
      return [w, w, s[1], s[2]];
    });
  }

  function TextViews(text, cfg) {
    var self = this;
    this.text = text;
    this.vocab = new Map([['', 0]]);
    this.views = [];
    this.warnings = [];
    this.nMerged = 0;
    var bySig = new Map();
    var starts = [];
    cfg.starts.forEach(function (s) {
      if (s === 'body' && text.paragraphs.length < 2) {
        self.warnings.push("start 'body' skipped: " + text.label + ' has no paragraph after the title');
        return;
      }
      starts.push([s, null]);
    });
    cfg.markers.forEach(function (m) {
      var found = text.findMarker(m);
      if (!found) self.warnings.push('marker "' + m + '" not found in ' + text.label + '; that start point is skipped for this text');
      else starts.push(['marker:' + m, found]);
    });
    cfg.units.forEach(function (unit) {
      var toks = unit === 'word' ? cfg.tokenizers : [null];
      toks.forEach(function (tok) {
        var items = text.paragraphs.map(function (p) { return unitItems(p, unit, tok); });
        READS[unit].forEach(function (read) {
          var kind = read === 'item' ? 'item' : 'letter';
          if (cfg.mode === 'letters' && kind === 'item') return;
          var codes = [], disp = [];
          items.forEach(function (its) {
            var arr = new Int32Array(its.length);
            for (var k = 0; k < its.length; k++) arr[k] = kind === 'item' ? self._vid(fold(its[k][1])) : letterCode(its[k][1]);
            codes.push(arr);
            disp.push(its.map(function (it) { return it[0]; }));
          });
          starts.forEach(function (st) {
            var sname = st[0], found = st[1], start;
            if (!found) start = ['slot', sname === 'title' ? 0 : 1];
            else {
              var pi = found[0], ls = found[1], off = items[pi].length;
              for (var k = 0; k < items[pi].length; k++) if (items[pi][k][3] > ls) { off = k; break; }
              start = (pi === 0 && off === 0) ? ['slot', 0] : ['anchor', pi, off];
            }
            var parts = [unit].concat(tok ? [tok] : [], [read, 'from=' + sname]);
            var v = new View(parts[0] + parts.slice(1).map(function (x) { return ' | ' + x; }).join(''), kind, codes, disp, start);
            if (bySig.has(v.signature)) { self.views[bySig.get(v.signature)].aliases.push(v.name); self.nMerged++; }
            else { bySig.set(v.signature, self.views.length); self.views.push(v); }
          });
        });
      });
    });
  }
  TextViews.prototype._vid = function (key) {
    if (!this.vocab.has(key)) this.vocab.set(key, this.vocab.size);
    return this.vocab.get(key);
  };
  TextViews.prototype.vocabList = function () {
    var out = new Array(this.vocab.size);
    this.vocab.forEach(function (i, k) { out[i] = k; });
    return out;
  };

  function buildConventions(tv, ds, cfg) {
    var groups = distinctGroupings(ds, cfg.groupings), convs = [];
    tv.views.forEach(function (v, vi) {
      groups.forEach(function (ga, gi) {
        cfg.bases.forEach(function (b) {
          var aliases = [];
          v.aliases.forEach(function (vn) { ga.forEach(function (g) { aliases.push(vn + ' | ' + b + '-based | digits=' + g); }); });
          convs.push({ viewIndex: vi, groupIndex: gi, grouping: ga[0], base: b,
            name: v.name + ' | ' + b + '-based | digits=' + ga[0], aliases: aliases, unit: v.name.split(' ')[0] });
        });
      });
    });
    return { convs: convs, groups: groups };
  }

  // ------------------------------------------------------------------
  // Scores (scoring.py)
  // ------------------------------------------------------------------

  var MAX_WORD = 13;

  function uniqueKeys(words) {
    var seen = new Set(), out = [];
    words.forEach(function (w) { var k = fold(w); if (k && !seen.has(k)) { seen.add(k); out.push(k); } });
    return out;
  }

  function parseList(text) {
    return normalize(text || '').split('\n').map(strip).filter(function (l) { return l && l.charAt(0) !== '#'; });
  }

  function TargetScorer(targets, vocab) {
    this.keys = uniqueKeys(targets);
    if (!this.keys.length) throw new Error('The list of place names (targets) is empty.');
    var V = vocab.length, keys = this.keys;
    this.V = V;
    this.single = new Int32Array(V).fill(-1);
    var tnum = new Map();
    keys.forEach(function (k, i) { tnum.set(k, i); });
    for (var v = 0; v < V; v++) if (vocab[v] && tnum.has(vocab[v])) this.single[v] = tnum.get(vocab[v]);
    this.vlen = new Int32Array(V);
    for (v = 0; v < V; v++) this.vlen[v] = vocab[v].length;
    this.multi = [];
    for (var ti = 0; ti < keys.length; ti++) {
      var t = keys[ti], ok = new Uint8Array(t.length * V), any0 = false;
      for (v = 0; v < V; v++) {
        var k = vocab[v];
        if (!k || t.indexOf(k) < 0) continue;
        for (var off = 0; off < t.length; off++) {
          if (t.startsWith(k, off) && (off > 0 || k.length < t.length)) { ok[off * V + v] = 1; if (off === 0) any0 = true; }
        }
      }
      if (any0) this.multi.push([ti, t.length, ok]);
    }
    this.letterTargets = keys.map(function (t) { return Array.from(t).map(function (c) { return c.charCodeAt(0) - 97; }); });
    this.found = new Uint8Array(keys.length);
  }
  TargetScorer.prototype.mode = 'targets';
  TargetScorer.prototype.score = function (kind, codes, K) {
    var found = this.found, T = this.keys.length, j, k, c;
    found.fill(0);
    if (kind === 'item') {
      for (k = 0; k < K; k++) { c = codes[k]; if (c >= 0 && this.single[c] >= 0) found[this.single[c]] = 1; }
      var V = this.V, vlen = this.vlen;
      for (var mi = 0; mi < this.multi.length; mi++) {
        var ti = this.multi[mi][0], tlen = this.multi[mi][1], ok = this.multi[mi][2];
        for (j = 0; j < K - 1; j++) {
          var off = 0;
          for (k = j; k < K; k++) {
            c = codes[k];
            if (c < 0 || !ok[Math.min(off, tlen - 1) * V + c]) break;
            off += vlen[c];
            if (off === tlen && k > j) found[ti] = 1;
            if (off >= tlen) break;
          }
        }
      }
    } else {
      for (var t = 0; t < T; t++) {
        var tg = this.letterTargets[t], m = tg.length;
        for (j = 0; j + m <= K; j++) {
          var all = true;
          for (var i = 0; i < m; i++) if (codes[j + i] !== tg[i]) { all = false; break; }
          if (all) { found[t] = 1; break; }
        }
      }
    }
    var s = 0;
    for (t = 0; t < T; t++) s += found[t];
    this.lastHit = s >= 1;
    return s;
  };

  function LetterScorer(words) {
    var keys = uniqueKeys(words).filter(function (k) { return k.length <= MAX_WORD; });
    if (!keys.length) throw new Error('The word list is empty.');
    this.nWords = keys.length;
    // trie over a-z
    var child = [new Int32Array(26).fill(-1)], term = [0];
    var maxlen = 0;
    keys.forEach(function (k) {
      var node = 0;
      for (var i = 0; i < k.length; i++) {
        var c = k.charCodeAt(i) - 97;
        if (child[node][c] < 0) { child[node][c] = child.length; child.push(new Int32Array(26).fill(-1)); term.push(0); }
        node = child[node][c];
      }
      term[node] = 1;
      if (k.length > maxlen) maxlen = k.length;
    });
    this.child = new Int32Array(child.length * 26);
    for (var n = 0; n < child.length; n++) this.child.set(child[n], n * 26);
    this.term = Uint8Array.from(term);
    this.maxlen = maxlen;
    this.best = new Float64Array(MAX_DIGITS + 2);
  }
  LetterScorer.prototype.mode = 'letters';
  LetterScorer.prototype.score = function (kind, codes, K) {
    if (kind !== 'letter') throw new Error('letter scoring only applies to letter extracts');
    var best = this.best, child = this.child, term = this.term, s, m, n = 0;
    for (s = 0; s <= K; s++) best[s] = 0;
    for (s = 0; s < K; s++) {
      if (codes[s] >= 0) n++;
      if (best[s] > best[s + 1]) best[s + 1] = best[s];
      var node = 0, lim = Math.min(this.maxlen, K - s);
      for (m = 1; m <= lim; m++) {
        var c = codes[s + m - 1];
        if (c < 0) break;
        node = child[node * 26 + c];
        if (node < 0) break;
        if (term[node]) {
          var cand = best[s] + m * m * 1024 + m;
          if (cand > best[s + m]) best[s + m] = cand;
        }
      }
    }
    var sc = Math.floor(best[K] / 1024), cov = best[K] % 1024;
    this.lastHit = n >= 3 && cov * 5 >= n * 4;
    return sc;
  };

  // ------------------------------------------------------------------
  // Engine (engine.py)
  // ------------------------------------------------------------------

  // Item codes at 0-based positions; -1 = nothing there.  order = null for
  // the text as written, else a paragraph order with order[0] === 0.
  function gatherInto(view, pos, K, order, out, seg) {
    var k, p;
    if (!order) {
      var total = view.flat.length - view.startFlat;
      for (k = 0; k < K; k++) { p = pos[k]; out[k] = (p >= 0 && p < total) ? view.flat[view.startFlat + p] : -1; }
      return out;
    }
    var P = order.length, lens = seg.lens, offs = seg.offs, cum = seg.cum, s;
    for (s = 0; s < P; s++) { lens[s] = view.paraLen[order[s]]; offs[s] = 0; }
    if (view.start[0] === 'slot') { for (s = 0; s < view.start[1]; s++) lens[s] = 0; }
    else {
      var m = view.start[1], o = view.start[2], sm = 0;
      while (order[sm] !== m) sm++;
      for (s = 0; s < sm; s++) lens[s] = 0;
      lens[sm] = view.paraLen[m] - o; offs[sm] = o;
    }
    var acc = 0;
    for (s = 0; s < P; s++) { acc += lens[s]; cum[s] = acc; }
    for (k = 0; k < K; k++) {
      p = pos[k];
      if (p < 0 || p >= acc) { out[k] = -1; continue; }
      var lo = 0, hi = P - 1;
      while (lo < hi) { var mid = (lo + hi) >> 1; if (cum[mid] > p) hi = mid; else lo = mid + 1; }
      var before = cum[lo] - lens[lo];
      out[k] = view.flat[view.paraBase[order[lo]] + offs[lo] + (p - before)];
    }
    return out;
  }

  function randomOrder(rng, P, out) {
    out[0] = 0;
    for (var i = 1; i < P; i++) out[i] = i;
    for (i = P - 1; i > 1; i--) { var j = 1 + rng.int(i); var t = out[i]; out[i] = out[j]; out[j] = t; }
    return out;
  }

  function Analysis(text, ds, cfg, targets, wordlist) {
    this.text = text; this.ds = ds; this.cfg = cfg;
    this.tv = new TextViews(text, cfg);
    if (!this.tv.views.length) throw new Error('No ways of counting are left for ' + text.label + ' (check the restrictions).');
    var bc = buildConventions(this.tv, ds, cfg);
    this.convs = bc.convs; this.groups = bc.groups;
    this.scorer = cfg.mode === 'targets' ? new TargetScorer(targets || [], this.tv.vocabList()) : new LetterScorer(wordlist || []);
    this.M = this.convs.length;
    this.nParagraphs = text.paragraphs.length;
    var nv = this.tv.views.length, nb = cfg.bases.length;
    this.col = new Int32Array(this.groups.length * nb * nv);
    for (var i = 0; i < this.M; i++) {
      var c = this.convs[i];
      this.col[(c.groupIndex * nb + cfg.bases.indexOf(c.base)) * nv + c.viewIndex] = i;
    }
    var P = this.nParagraphs;
    this._seg = { lens: new Int32Array(P), offs: new Int32Array(P), cum: new Int32Array(P) };
    this._codes = new Int32Array(MAX_DIGITS);
    this._pos = new Float64Array(MAX_DIGITS);
  }
  Analysis.prototype.positions = function (d, gi, base) {
    return numbers(this.groups[gi][0], d, this.ds.lengths).map(function (x) { return x - base; });
  };
  // Scores (Int32Array M) and hits (Uint8Array M) for one digit row.
  Analysis.prototype.evaluate = function (d, order, scores, hits) {
    scores = scores || new Int32Array(this.M);
    hits = hits || new Uint8Array(this.M);
    var views = this.tv.views, sc = this.scorer, codes = this._codes, pos = this._pos;
    for (var gi = 0; gi < this.groups.length; gi++) {
      var nums = numbers(this.groups[gi][0], d, this.ds.lengths), K = nums.length;
      for (var bi = 0; bi < this.cfg.bases.length; bi++) {
        var b = this.cfg.bases[bi];
        for (var k = 0; k < K; k++) pos[k] = nums[k] - b;
        for (var vi = 0; vi < views.length; vi++) {
          gatherInto(views[vi], pos, K, order, codes, this._seg);
          var j = this.col[(gi * this.cfg.bases.length + bi) * views.length + vi];
          scores[j] = sc.score(views[vi].kind, codes, K);
          hits[j] = sc.lastHit ? 1 : 0;
        }
      }
    }
    return { scores: scores, hits: hits };
  };
  Analysis.prototype.observed = function () { return this.evaluate(this.ds.digits(), null); };
  // which: 'A' (random digits) or 'B' (shuffled paragraphs); stream 0 = reference, 1 = test
  Analysis.prototype.nullDraws = function (which, draws, seed, stream, progress) {
    var rng = makeRng([seed, which === 'A' ? 1 : 2, stream]);
    var M = this.M, S = new Int32Array(draws * M), nhit = new Int32Array(draws);
    var d = this.ds.digits(), order = null, P = this.nParagraphs;
    var scores = new Int32Array(M), hits = new Uint8Array(M);
    if (which === 'B' && P >= 3) order = new Int32Array(P);
    for (var i = 0; i < draws; i++) {
      if (which === 'A') this.ds.randomDigits(rng, d);
      else if (order) randomOrder(rng, P, order);
      this.evaluate(d, order, scores, hits);
      S.set(scores, i * M);
      var h = 0;
      for (var j = 0; j < M; j++) h += hits[j];
      nhit[i] = h;
      if (progress && (i % 500 === 499 || i === draws - 1)) progress(which, stream, i + 1, draws);
    }
    return { S: S, nhit: nhit, N: draws };
  };
  Analysis.prototype.extract = function (ci) {
    var c = this.convs[ci], v = this.tv.views[c.viewIndex];
    var d = this.ds.digits();
    var pos = this.positions(d, c.groupIndex, c.base);
    var total = v.flat.length - v.startFlat, items = [], letters = [];
    pos.forEach(function (p) {
      if (p >= 0 && p < total) {
        var disp = v.disp[v.startFlat + p], code = v.flat[v.startFlat + p];
        items.push(disp ? disp : '∅');
        letters.push(v.kind === 'letter' && code >= 0 ? String.fromCharCode(97 + code).toUpperCase() : '·');
      } else { items.push('·'); letters.push('·'); }
    });
    return { numbers: this.positions(d, c.groupIndex, 0), items: items, letters: v.kind === 'letter' ? letters.join('') : null };
  };

  function median(a) {
    var s = Array.from(a).sort(function (x, y) { return x - y; }), n = s.length;
    return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
  }
  function percentile(a, q) {   // numpy default (linear)
    var s = Array.from(a).sort(function (x, y) { return x - y; }), h = (s.length - 1) * q / 100;
    var lo = Math.floor(h), hi = Math.ceil(h);
    return s[lo] + (s[hi] - s[lo]) * (h - lo);
  }

  // How unusual is a score for one convention? (engine.py TailModel)
  function TailModel(R, NR, M) {
    this.NR = NR; this.M = M;
    var top = 0, i, j, v;
    for (i = 0; i < R.length; i++) if (R[i] > top) top = R[i];
    var W = top + 2;
    this.W = W;
    var cnt = new Int32Array(M * W);
    for (i = 0; i < NR; i++) for (j = 0; j < M; j++) cnt[j * W + R[i * M + j]]++;
    for (j = 0; j < M; j++) for (v = W - 2; v >= 0; v--) cnt[j * W + v] += cnt[j * W + v + 1];
    this.cnt = cnt;
    this.vb = new Int32Array(M);
    var lam = new Float64Array(M), okList = [];
    for (j = 0; j < M; j++) {
      var vb = 0, va = 0;
      for (v = 0; v < W; v++) { if (cnt[j * W + v] >= 10) vb = v; if (cnt[j * W + v] >= 100) va = v; }
      this.vb[j] = vb;
      if (vb > va) {
        lam[j] = Math.log((cnt[j * W + va] + 1.0) / (cnt[j * W + vb] + 1.0)) / (vb - va);
        okList.push(lam[j]);
      } else lam[j] = NaN;
    }
    var fallback = okList.length ? median(okList) : Math.log(10.0);
    for (j = 0; j < M; j++) if (isNaN(lam[j])) lam[j] = fallback;
    this.lam = lam;
    this.logNorm = Math.log(NR + 1.0);
  }
  TailModel.prototype.logRarity = function (scores, j) {
    var x = scores[j], vb = this.vb[j], xc = x < vb ? x : vb;
    return Math.log(this.cnt[j * this.W + xc] + 1.0) - this.logNorm - this.lam[j] * Math.max(0, x - vb);
  };
  TailModel.prototype.statistic = function (scores) {
    var best = Infinity;
    for (var j = 0; j < this.M; j++) { var r = this.logRarity(scores, j); if (r < best) best = r; }
    return best;
  };

  function NullTest(ref, test, M) {
    this.tail = new TailModel(ref.S, ref.N, M);
    this.N = test.N;
    this.nullStat = new Float64Array(test.N);
    for (var i = 0; i < test.N; i++) this.nullStat[i] = this.tail.statistic(test.S.subarray(i * M, (i + 1) * M));
  }
  NullTest.prototype.p = function (scores, u) {
    var f = this.tail.statistic(scores), le = 0, lt = 0, eq = 0;
    for (var i = 0; i < this.N; i++) { var x = this.nullStat[i]; if (x <= f) le++; if (x < f) lt++; else if (x === f) eq++; }
    if (u === undefined || u === null) return (1.0 + le) / (1.0 + this.N);
    return (lt + u * (eq + 1.0)) / (1.0 + this.N);
  };

  function analyse(text, ds, cfg, draws, seed, opts) {
    opts = opts || {};
    if (draws < MIN_DRAWS) throw new Error('At least ' + MIN_DRAWS + ' null draws are required.');
    var an = new Analysis(text, ds, cfg, opts.targets, opts.wordlist);
    var obs = an.observed(), M = an.M;
    var obsS = Int32Array.from(obs.scores), obsH = Uint8Array.from(obs.hits);
    var tests = {};
    ['A', 'B'].forEach(function (which) {
      var ref = an.nullDraws(which, draws, seed, 0, opts.progress);
      var test = an.nullDraws(which, draws, seed, 1, opts.progress);
      tests[which] = { nt: new NullTest(ref, test, M), test: test };
    });
    var nA = tests.A.nt, nB = tests.B.nt;
    var pA = nA.p(obsS), pB = nB.p(obsS);
    var rar = new Float64Array(M);
    for (var j = 0; j < M; j++) rar[j] = nA.tail.logRarity(obsS, j);
    var order = [];
    for (j = 0; j < M; j++) order.push(j);
    order.sort(function (a, b) { return (rar[a] - rar[b]) || (obsS[b] - obsS[a]) || (a - b); });
    var top = order.slice(0, 5).map(function (i) {
      var e = an.extract(i);
      return { name: an.convs[i].name, aliases: an.convs[i].aliases, score: obsS[i], hit: !!obsH[i],
        rarity: Math.exp(rar[i]), numbers: e.numbers, items: e.items, letters: e.letters };
    });
    var best = order[0], winners = [];
    for (j = 0; j < M; j++) if (rar[j] === rar[best] && obsS[j] > 0) winners.push(j);
    var rawMax = function (t) { var out = new Int32Array(t.N); for (var i = 0; i < t.N; i++) { var m = 0; for (var k = 0; k < M; k++) if (t.S[i * M + k] > m) m = t.S[i * M + k]; out[i] = m; } return out; };
    var byUnit = {};
    cfg.units.forEach(function (u) { byUnit[u] = an.convs.filter(function (c) { return c.unit === u; }).length; });
    var nh = 0;
    for (j = 0; j < M; j++) nh += obsH[j];
    var hitsA = tests.A.test.nhit;
    var result = {
      label: text.label, path: text.path, sha256: text.sha256,
      paragraphs: text.paragraphs.length, words: text.wordCount(),
      M: M, merged_views: an.tv.nMerged, n_views: an.tv.views.length,
      groupings: an.groups, warnings: an.tv.warnings.slice(), by_unit: byUnit,
      conventions: an.convs.map(function (c) { return c.name; }), draws: draws,
      best_name: an.convs[best].name, best_score: obsS[best], best_rarity: Math.exp(rar[best]),
      raw_max: Math.max.apply(null, Array.from(obsS)),
      nullA_raw_max_median: median(rawMax(tests.A.test)), nullB_raw_max_median: median(rawMax(tests.B.test)),
      hits: nh, nullA_mean_hits: hitsA.reduce(function (a, b) { return a + b; }, 0) / hitsA.length,
      nullA_hits_95: Math.floor(percentile(hitsA, 95)),
      pA: pA, pB: pB, p: Math.max(pA, pB), shuffle_possible: an.nParagraphs >= 3,
      top: top, winners: winners.map(function (i) { return an.convs[i].aliases; }), n_winners: winners.length
    };
    if (opts.returnRaw) return { result: result, analysis: an, nullA: nA, nullB: nB, obs: obsS };
    return result;
  }

  // ------------------------------------------------------------------
  // Kolmogorov-Smirnov against uniform (stats.py)
  // ------------------------------------------------------------------

  function ksUniform(values) {
    var x = Array.from(values).sort(function (a, b) { return a - b; }), n = x.length, d = 0;
    for (var i = 0; i < n; i++) d = Math.max(d, (i + 1) / n - x[i], x[i] - i / n);
    var en = Math.sqrt(n), lam = (en + 0.12 + 0.11 / en) * d;
    if (lam < 1e-3) return [d, 1.0];
    var p = 0;
    for (var k = 1; k <= 100; k++) {
      var term = 2.0 * (k % 2 ? 1 : -1) * Math.exp(-2.0 * k * k * lam * lam);
      p += term;
      if (Math.abs(term) < 1e-12) break;
    }
    return [d, Math.min(1, Math.max(0, p))];
  }

  // ------------------------------------------------------------------
  // SHA-256 (for fingerprints of texts and locked tests)
  // ------------------------------------------------------------------

  function utf8(s) { return new TextEncoder().encode(s); }

  var K256 = new Uint32Array([
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]);

  function sha256Hex(bytes) {
    var n = bytes.length, total = ((n + 9 + 63) >> 6) << 6, buf = new Uint8Array(total);
    buf.set(bytes); buf[n] = 0x80;
    var bits = n * 8, dv = new DataView(buf.buffer);
    dv.setUint32(total - 4, bits >>> 0); dv.setUint32(total - 8, Math.floor(bits / 4294967296));
    var h = new Uint32Array([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]);
    var w = new Uint32Array(64);
    for (var off = 0; off < total; off += 64) {
      for (var i = 0; i < 16; i++) w[i] = dv.getUint32(off + i * 4);
      for (i = 16; i < 64; i++) {
        var a0 = w[i - 15], a1 = w[i - 2];
        var s0 = ((a0 >>> 7) | (a0 << 25)) ^ ((a0 >>> 18) | (a0 << 14)) ^ (a0 >>> 3);
        var s1 = ((a1 >>> 17) | (a1 << 15)) ^ ((a1 >>> 19) | (a1 << 13)) ^ (a1 >>> 10);
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) >>> 0;
      }
      var a = h[0], b = h[1], c = h[2], d = h[3], e = h[4], f = h[5], g = h[6], hh = h[7];
      for (i = 0; i < 64; i++) {
        var S1 = ((e >>> 6) | (e << 26)) ^ ((e >>> 11) | (e << 21)) ^ ((e >>> 25) | (e << 7));
        var ch = (e & f) ^ (~e & g);
        var t1 = (hh + S1 + ch + K256[i] + w[i]) >>> 0;
        var S0 = ((a >>> 2) | (a << 30)) ^ ((a >>> 13) | (a << 19)) ^ ((a >>> 22) | (a << 10));
        var mj = (a & b) ^ (a & c) ^ (b & c);
        var t2 = (S0 + mj) >>> 0;
        hh = g; g = f; f = e; e = (d + t1) >>> 0; d = c; c = b; b = a; a = (t1 + t2) >>> 0;
      }
      h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += g; h[7] += hh;
    }
    return Array.from(h).map(function (x) { return ('00000000' + x.toString(16)).slice(-8); }).join('');
  }

  // Stable JSON (sorted keys) so a locked test always hashes the same.
  function canonicalJSON(v) {
    if (Array.isArray(v)) return '[' + v.map(canonicalJSON).join(',') + ']';
    if (v && typeof v === 'object') {
      return '{' + Object.keys(v).sort().map(function (k) { return JSON.stringify(k) + ':' + canonicalJSON(v[k]); }).join(',') + '}';
    }
    return JSON.stringify(v === undefined ? null : v);
  }


  // ------------------------------------------------------------------
  // Self-test (selftest.py): planted messages must be found, random
  // inputs must come out uniformly non-significant.
  // demo = { en: text, fr: text, targets: [...], wordlistEn: [...] }
  // ------------------------------------------------------------------

  var SELFTEST_SEED = 20240611, N_CALIB = 400;

  function selftest(demo, report) {
    var rows = [];
    var check = function (name, ok, detail) {
      rows.push({ name: name, ok: !!ok, detail: detail || '' });
      if (report) report({ type: 'check', name: name, ok: !!ok, detail: detail || '' });
    };
    var eq = function (a, b) { return JSON.stringify(a) === JSON.stringify(b); };
    var s = '« Bonjour » : l’Or de Val-d\'Or – fin.';
    check('tokenizer ws keeps standalone punctuation',
      eq(tokens(s, 'ws'), ['«', 'Bonjour', '»', ':', 'l’Or', 'de', "Val-d'Or", '–', 'fin.']));
    check('tokenizer ws-drop drops it', eq(tokens(s, 'ws-drop'), ['Bonjour', 'l’Or', 'de', "Val-d'Or", 'fin.']));
    check('tokenizer strip keeps inner apostrophes/hyphens', eq(tokens(s, 'strip'), ['Bonjour', 'l’Or', 'de', "Val-d'Or", 'fin']));
    check('tokenizer split splits elisions and hyphens', eq(tokens(s, 'split'), ['Bonjour', 'l', 'Or', 'de', 'Val', 'd', 'Or', 'fin']));
    check('folding: accents, both apostrophes, case',
      fold('VAL-D’OR') === 'valdor' && fold("Val-d'Or") === 'valdor' && fold('Hérons') === 'herons' && fold('cœur') === 'coeur');
    check('NFC: decomposed é is one letter', eq(tokens('Hérons', 'strip'), ['Hérons']));

    var en = Text.fromString('en', demo.en), fr = Text.fromString('fr', demo.fr);

    // fast path == shuffle path when nothing is shuffled
    var probe = new DigitString('12 345 6 78');
    var an = new Analysis(fr, probe, new Config({ mode: 'targets', markers: ['Son magasin'] }), demo.targets);
    var ident = new Int32Array(an.nParagraphs);
    for (var i = 0; i < ident.length; i++) ident[i] = i;
    var rng = makeRng([1, 1]), same = true, d = new Array(probe.nDigits), o1 = new Int32Array(MAX_DIGITS), o2 = new Int32Array(MAX_DIGITS);
    for (var r = 0; r < 7 && same; r++) {
      probe.randomDigits(rng, d);
      an.tv.views.forEach(function (v) {
        an.groups.forEach(function (g, gi) {
          [0, 1].forEach(function (b) {
            var pos = an.positions(d, gi, b);
            gatherInto(v, pos, pos.length, null, o1, an._seg);
            gatherInto(v, pos, pos.length, ident, o2, an._seg);
            for (var k = 0; k < pos.length; k++) if (o1[k] !== o2[k]) same = false;
          });
        });
      });
    }
    check('shuffle path == plain path when nothing is shuffled', same);

    var progress = function (label) {
      return function (which, stream, done, total) {
        if (report) report({ type: 'progress', label: label, which: which, stream: stream, done: done, total: total });
      };
    };

    // planted letters
    rng = makeRng([SELFTEST_SEED, 3]);
    var words = [];
    en.paragraphs.slice(1).forEach(function (p) { tokenize(p, 'ws').forEach(function (t) { words.push(t[0]); }); });
    var message = 'goldisnorth', picks = [];
    Array.from(message).forEach(function (ch) {
      var cands = [];
      words.forEach(function (w, i) { if (fold(w).charAt(0) === ch && i + 1 >= 10) cands.push(i + 1); });
      picks.push(cands[rng.int(cands.length)]);
    });
    var ds = new DigitString(picks.join(' '));
    var raw = analyse(en, ds, new Config({ mode: 'letters' }), MIN_DRAWS, SELFTEST_SEED,
      { wordlist: demo.wordlistEn, returnRaw: true, progress: progress('planted letters') });
    var res = raw.result, planted = 'word | ws | initial | from=body | 1-based | digits=given';
    check('planted letters: found by the planted convention',
      res.winners.some(function (a) { return a.indexOf(planted) >= 0; }), 'top: ' + res.top[0].name + ' -> ' + res.top[0].letters);
    check('planted letters: p <= 0.01', res.p <= 0.01, 'pA=' + res.pA.toFixed(5) + ' pB=' + res.pB.toFixed(5));
    calibrate(check, 'letters', raw, ds, SELFTEST_SEED);

    // planted targets: split tokenizer, 0-based from the title, cumulative steps
    var fw = [];
    fr.paragraphs.forEach(function (p) { tokenize(p, 'split').forEach(function (t) { fw.push(fold(t[0])); }); });
    var last = -1, posn = [];
    ['cuivre', 'cuivre', 'herons', 'sureau'].forEach(function (w) {
      for (var k = last + 1; k < fw.length; k++) if (fw[k] === w) { last = k; break; }
      posn.push(last);
    });
    var steps = [posn[0]];
    for (i = 1; i < posn.length; i++) steps.push(posn[i] - posn[i - 1]);
    ds = new DigitString(steps.join('-'));
    raw = analyse(fr, ds, new Config({ mode: 'targets' }), MIN_DRAWS, SELFTEST_SEED,
      { targets: demo.targets, returnRaw: true, progress: progress('planted targets') });
    res = raw.result;
    planted = 'word | split | item | from=title | 0-based | digits=cumulative';
    check('planted targets: found by the planted convention',
      res.winners.some(function (a) { return a.indexOf(planted) >= 0; }), 'top: ' + res.top[0].name + ' -> ' + res.top[0].items.join(' '));
    check('planted targets: p <= 0.01', res.p <= 0.01, 'pA=' + res.pA.toFixed(5) + ' pB=' + res.pB.toFixed(5));
    calibrate(check, 'targets', raw, ds, SELFTEST_SEED + 1);

    return { passed: rows.every(function (x) { return x.ok; }), checks: rows };
  }

  function calibrate(check, name, raw, ds, seed) {
    var an = raw.analysis, rng = makeRng([seed, 99]), urng = makeRng([seed, 98]);
    var d = ds.digits(), order = new Int32Array(an.nParagraphs);
    var scores = new Int32Array(an.M), hits = new Uint8Array(an.M);
    [['A', raw.nullA], ['B', raw.nullB]].forEach(function (pair) {
      var which = pair[0], nt = pair[1], prand = [], pcons = [];
      for (var i = 0; i < N_CALIB; i++) {
        if (which === 'A') an.evaluate(ds.randomDigits(rng, d), null, scores, hits);
        else an.evaluate(ds.digits(), an.nParagraphs >= 3 ? randomOrder(rng, an.nParagraphs, order) : null, scores, hits);
        prand.push(nt.p(scores, urng.random()));
        pcons.push(nt.p(scores));
      }
      var ks = ksUniform(prand), hist = new Array(10).fill(0);
      prand.forEach(function (p) { hist[Math.min(9, Math.floor(p * 10))]++; });
      check(name + ' null ' + which + ': p-values of ' + N_CALIB + ' random inputs look uniform', ks[1] >= 0.01,
        'KS D=' + ks[0].toFixed(3) + ', p=' + ks[1].toFixed(3) + '; deciles ' + hist.join(' '));
      [0.05, 0.01].forEach(function (a) {
        var nsig = pcons.filter(function (p) { return p <= a; }).length;
        var limit = N_CALIB * a + 3 * Math.sqrt(N_CALIB * a * (1 - a));
        check(name + ' null ' + which + ': random inputs significant at ' + a.toFixed(2), nsig <= limit,
          nsig + ' of ' + N_CALIB + ' (allowed up to ' + Math.round(limit) + ')');
      });
    });
  }

  var API = {
    VERSION: VERSION, MIN_DRAWS: MIN_DRAWS,
    normalize: normalize, fold: fold, letterCode: letterCode, tokenize: tokenize, tokens: tokens,
    lineSpans: lineSpans, sentenceSpans: sentenceSpans, Text: Text,
    TOKENIZERS: TOKENIZERS, TOKENIZER_HELP: TOKENIZER_HELP,
    GROUPINGS: GROUPINGS, GROUPING_HELP: GROUPING_HELP, DigitString: DigitString, numbers: numbers,
    distinctGroupings: distinctGroupings,
    UNITS: UNITS, UNIT_HELP: UNIT_HELP, READS: READS, BASES: BASES, DEFAULT_STARTS: DEFAULT_STARTS,
    Config: Config, TextViews: TextViews, buildConventions: buildConventions,
    TargetScorer: TargetScorer, LetterScorer: LetterScorer, uniqueKeys: uniqueKeys, parseList: parseList,
    gatherInto: gatherInto, randomOrder: randomOrder, makeRng: makeRng,
    Analysis: Analysis, TailModel: TailModel, NullTest: NullTest, analyse: analyse,
    ksUniform: ksUniform, selftest: selftest, sha256Hex: sha256Hex, utf8: utf8, canonicalJSON: canonicalJSON
  };
  root.IndexKit = API;
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
})(typeof self !== 'undefined' ? self : this);
