// unbot-voice scanner, browser edition. Mirrors skills/unbot-voice/scripts/scan.py and
// uses the same patterns.json, so scores match the CLI.
(function (root) {
  "use strict";

  const CATEGORIES = ["residue", "forced-voice", "content", "language", "style"];
  const QUOTED = /"[^"\n]{1,80}"|“[^”\n]{1,80}”|`[^`\n]{1,80}`/g;
  const CODE_FENCE = /^(```|~~~)[\s\S]*?^\1/gm;
  const SENT_SPLIT = /(?<=[.!?])\s+(?=[A-Z"'(])/;
  const LIST_LINE = /(^|\n)\s*([-*#>|]|\d+\.)\s.*/g;
  const WORD = /[\p{L}\p{N}_]+/gu;

  function compile(data) {
    return data.patterns.map((p) => ({
      category: p.category,
      label: p.label,
      weight: p.weight,
      tip: p.tip || "",
      rx: new RegExp(p.regex, "gimu"),
    }));
  }

  const blank = (m) => m.replace(/[^\n]/g, " ");

  function mask(text, includeQuotes) {
    let t = text.replace(CODE_FENCE, blank);
    if (!includeQuotes) t = t.replace(QUOTED, blank);
    return t;
  }

  function sentenceLengths(text) {
    const prose = text.replace(LIST_LINE, "").trim();
    if (!prose) return [];
    return prose
      .split(SENT_SPLIT)
      .map((s) => s.split(/\s+/).filter(Boolean).length)
      .filter((n) => n >= 3);
  }

  function band(score) {
    if (score < 10) return { key: "low", text: "few tells" };
    if (score < 25) return { key: "moderate", text: "some tells, worth a pass" };
    if (score < 50) return { key: "high", text: "reads as AI-assisted" };
    return { key: "very-high", text: "reads as unedited AI output" };
  }

  function scan(text, compiled, opts) {
    const includeQuotes = !!(opts && opts.includeQuotes);
    const scanned = mask(text, includeQuotes);
    const words = (scanned.match(WORD) || []).length;
    const hits = [];
    for (const p of compiled) {
      p.rx.lastIndex = 0;
      let m;
      while ((m = p.rx.exec(scanned)) !== null) {
        if (m[0].length === 0) { p.rx.lastIndex++; continue; }
        if (!m[0].trim()) continue;
        // Report the span without leading whitespace/newlines, for highlighting.
        const lead = m[0].length - m[0].replace(/^\s+/, "").length;
        const start = m.index + lead;
        const end = m.index + m[0].replace(/\s+$/, "").length;
        hits.push({
          category: p.category,
          pattern: p.label,
          weight: p.weight,
          tip: p.tip,
          match: m[0].split(/\s+/).filter(Boolean).join(" "),
          start,
          end,
          line: scanned.slice(0, m.index).split("\n").length,
        });
      }
    }

    const em = (scanned.match(/—/g) || []).length + (scanned.match(/\s--\s/g) || []).length;
    const lengths = sentenceLengths(scanned);
    const stats = { words, sentences: lengths.length, emDashes: em };
    const flags = [];
    let rhythm = false;
    if (lengths.length >= 5) {
      const mean = lengths.reduce((a, b) => a + b, 0) / lengths.length;
      const sd = Math.sqrt(lengths.reduce((a, b) => a + (b - mean) ** 2, 0) / lengths.length);
      stats.meanSentenceLen = Math.round(mean * 10) / 10;
      stats.sentenceLenStdev = Math.round(sd * 10) / 10;
      if (sd / mean < 0.35) {
        rhythm = true;
        flags.push(`Sentences are all about the same length (${sd.toFixed(1)} word spread around a ${mean.toFixed(1)} word average). Vary the rhythm.`);
      }
    }
    const perK = 1000 / Math.max(words, 1);
    const emRate = em * perK;
    const emFlag = em >= 2 && emRate > 4;
    if (emFlag) flags.unshift(`${em} em dashes (${emRate.toFixed(1)} per 1,000 words).`);

    let score = hits.reduce((a, h) => a + h.weight, 0) * perK;
    if (emFlag) score += Math.min(emRate, 15);
    if (rhythm) score += 5;
    score = Math.round(score * 10) / 10;
    return { score, band: band(score), stats, flags, hits };
  }

  const api = { CATEGORIES, compile, scan, band };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.Unbot = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
