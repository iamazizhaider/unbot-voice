// unbot-voice auto-fixer, browser edition. Applies the safe, mechanical fixes only:
// deletions of chatbot residue and filler, plain-word swaps, and punctuation habits.
// Anything that needs facts or judgment (inflated claims, weasel sources, placeholders,
// "not X but Y") is left alone so the rescan can list it for the writer.
(function (root) {
  "use strict";

  const CAP = "\u0001"; // marker: capitalize the next letter after a deletion
  const LOW = "\u0002"; // marker: lowercase the next word unless it's an acronym
  const SS = "(^|[.!?]\\s+|\\n[ \\t]*|\\u0001)"; // sentence start (or a prior deletion), kept as $1

  // Replace whole sentences (to the next terminator) that contain a phrase.
  const sentence = (phrase) => new RegExp(`${SS}[^.!?\\n]*?\\b(?:${phrase})[^.!?\\n]*[.!?]*[ \\t]*`, "gi");
  // Drop a lead-in at the start of a sentence and capitalize what follows.
  const leadIn = (phrase) => [new RegExp(`${SS}(?:${phrase})\\s*`, "gi"), `$1${CAP}`];

  // Word swaps: [regex source, replacement]. Case of the first letter is preserved.
  const WORDS = [
    ["delve into", "look at"], ["delves into", "looks at"], ["delved into", "looked at"], ["delving into", "looking at"],
    ["delve", "dig"], ["delves", "digs"], ["delved", "dug"], ["delving", "digging"],
    ["utilize", "use"], ["utilizes", "uses"], ["utilized", "used"], ["utilizing", "using"],
    ["leverage", "use"], ["leverages", "uses"], ["leveraged", "used"], ["leveraging", "using"],
    ["commence", "start"], ["commences", "starts"], ["commenced", "started"],
    ["facilitate", "help"], ["facilitates", "helps"], ["facilitated", "helped"], ["facilitating", "helping"],
    ["showcase", "show"], ["showcases", "shows"], ["showcased", "showed"], ["showcasing", "showing"],
    ["enhance", "improve"], ["enhances", "improves"], ["enhanced", "improved"], ["enhancing", "improving"],
    ["elevate", "improve"], ["elevates", "improves"], ["elevating", "improving"],
    ["empower you to", "help you"], ["empowers you to", "helps you"], ["empower", "help"], ["empowers", "helps"],
    ["foster", "build"], ["fosters", "builds"], ["fostered", "built"], ["fostering", "building"],
    ["bolster", "strengthen"], ["bolsters", "strengthens"], ["bolstered", "strengthened"],
    ["garner", "earn"], ["garners", "earns"], ["garnered", "earned"],
    ["embark on", "start"], ["embarks on", "starts"], ["embarked on", "started"],
    ["underscores", "shows"], ["underscored", "showed"], ["underscoring", "showing"],
    ["seamlessly", "smoothly"], ["seamless", "smooth"], ["robust", "solid"], ["cutting-edge", "modern"],
    ["meticulously", "carefully"], ["meticulous", "careful"], ["an intricate", "a complex"], ["intricate", "complex"], ["multifaceted", "complex"],
    ["individuals", "people"], ["paramount", "essential"],
    ["a plethora of", "many"], ["a myriad of", "many"], ["myriad", "many"],
    ["in order to ensure", "to make sure"], ["in order to", "to"],
    ["serves as", "is"], ["stands as", "is"], ["functions as", "is"], ["acts as a", "is a"],
    ["served as", "was"], ["boasts", "has"],
    ["a deep dive", "a close look"], ["more than just a", "more than a"],
    ["forward-thinking companies like yours", "companies like yours"], ["innovative companies like yours", "companies like yours"],
    ["was truly impressed", "was impressed"], ["truly", ""],
  ];

  const RULES = [
    // Chatbot residue and email boilerplate: delete the sentence.
    [sentence("i hope this helps|happy to help|great question|i hope (?:this|my) (?:email|message|note) finds you well"), "$1"],
    [sentence("would you like me to|let me know if you|feel free to (?:reach out|ask)|if you'd like, i can"), "$1"],
    [sentence("as an ai\\b|as a (?:large )?language model|as of my (?:last )?(?:knowledge|training) (?:update|cutoff)"), "$1"],
    [/(^|[.!?]\s+|\n[ \t]*)(?:certainly|absolutely)!\s*/gi, `$1${CAP}`],
    [sentence("let that sink in|read that again"), "$1"],
    // Tool artifacts.
    [/:?contentReference\[oaicite:\d+\]\{index=\d+\}/g, ""],
    [/\s*\[?oai_citation[^\]\s]*\]?/g, ""],
    [/[?&]utm_source=(?:chatgpt|openai)[\w.]*/gi, ""],
    // Manufactured drama.
    leadIn("here's the (?:thing|deal|kicker|catch):?"),
    [/\bhere's the (?:thing|deal|kicker|catch):?\s*/gi, ""],
    [/\b(and|but) honestly\?\s*/gi, "$1 "],
    [/(^|[.!?]\s+|\n[ \t]*)honestly\?\s*/gi, `$1${CAP}`],
    [/\b(the) (result|answer|catch|secret)\?\s+/gi, `$1 $2: ${LOW}`],
    leadIn("hot take:|then i realized:"),
    // Stock openers and hedges.
    leadIn("in today's (?:fast-paced|ever-changing|digital|rapidly[- ]\\w+)(?: \\w+){0,3}?,|in the (?:dynamic|ever-evolving|fast-paced) (?:world|landscape|realm) of [^,.]{1,40},|in the realm of [^,.]{1,40},"),
    leadIn("it(?:'s| is) (?:important|worth|crucial) (?:to note|noting|to remember)(?: that)?,?"),
    leadIn("at the end of the day,"),
    leadIn("whether you're an? [^.,;]{1,40} or (?:an? )?[^.,;]{1,40},"),
    // Transitions and summary closers.
    [/(^|[.!?]\s+|\n[ \t]*)additionally,\s*/gi, "$1Also, "],
    leadIn("(?:furthermore|moreover),"),
    [/(^|[.!?]\s+|\n[ \t]*)consequently,\s*/gi, "$1So "],
    leadIn("(?:notably|importantly|ultimately),"),
    leadIn("(?:in (?:summary|conclusion)|overall|to sum up|in essence|all in all)[,:]"),
    // Tacked-on "-ing" tails: end the sentence before them.
    [/,\s+(?:highlighting|underscoring|emphasizing|showcasing|reflecting|symbolizing|ensuring|fostering|contributing to|cementing|solidifying|reinforcing|demonstrating)\b[^.!?\n]*/gi, ""],
    // Formatting habits.
    [/(^|\n)([ \t]*(?:[-*]|#+)?[ \t]*)[\u{1F300}-\u{1FAFF}☀-➿⭐⚡]️?\s*/gu, "$1$2"],
    [/(^|\n)([ \t]*[-*][ \t]+)\*\*([^*\n]{1,40}?)(:?)\*\*(:?)/g, "$1$2$3$4$5"],
    [/[ \t]*(?:—|[ \t]--)[ \t]*(it's|it is|that's)\b/gi, `. ${CAP}$1`],
    [/[ \t]*—[ \t]*|[ \t]+--[ \t]+/g, ", "],
  ];

  const wordRules = WORDS.map(([from, to]) => [new RegExp(`\\b${from.replace(/-/g, "[- ]")}\\b`, "gi"), to]);

  function matchCase(src, repl) {
    if (!repl) return "";
    return /^[A-Z]/.test(src) ? repl.charAt(0).toUpperCase() + repl.slice(1) : repl;
  }

  function fixChunk(t) {
    for (const [rx, to] of RULES) t = t.replace(rx, to);
    for (const [rx, to] of wordRules) t = t.replace(rx, (m) => matchCase(m, to));
    return t;
  }

  function tidy(t) {
    t = t.replace(new RegExp(`${CAP}([^\\p{L}\\n]*)(\\p{Ll})`, "gu"), (m, gap, ch) => gap + ch.toUpperCase());
    t = t.replace(new RegExp(`${LOW}(\\p{Lu})(?!\\p{Lu})`, "gu"), (m, a) => a.toLowerCase());
    t = t.split(CAP).join("").split(LOW).join("");
    return t
      .replace(/[ \t]{2,}/g, " ")
      .replace(/[ \t]+([,.;:!?])/g, "$1")
      .replace(/,\s*,/g, ",")
      .replace(/,([.!?])/g, "$1")
      .replace(/^[ \t]*,[ \t]*/gm, "")
      .replace(/[ \t]+$/gm, "")
      .replace(/\n{3,}/g, "\n\n")
      .replace(/^\s+|\s+$/g, "");
  }

  // Keep code fences (and, unless asked, short quotes) exactly as written.
  const PROTECT = /^(```|~~~)[\s\S]*?^\1|"[^"\n]{1,80}"|“[^”\n]{1,80}”|`[^`\n]{1,80}`/gm;
  const FENCE_ONLY = /^(```|~~~)[\s\S]*?^\1|`[^`\n]{1,80}`/gm;

  function fix(text, opts) {
    const rx = opts && opts.includeQuotes ? FENCE_ONLY : PROTECT;
    let out = "", last = 0, m;
    rx.lastIndex = 0;
    while ((m = rx.exec(text)) !== null) {
      out += fixChunk(text.slice(last, m.index)) + m[0];
      last = m.index + m[0].length;
    }
    out += fixChunk(text.slice(last));
    return tidy(out);
  }

  // Token-level Myers diff, for showing what changed.
  function tokens(s) { return s.match(/\s+|[\p{L}\p{N}_'’-]+|[^\s\p{L}\p{N}_]/gu) || []; }
  // Returns null when the texts are too different to diff cheaply; callers then show
  // the fixed text without change marks. Memory stays bounded at ~MAX_D^2 ints.
  const MAX_D = 2000;
  function diff(a, b) {
    const TA = tokens(a), TB = tokens(b);
    let pre = 0;
    while (pre < TA.length && pre < TB.length && TA[pre] === TB[pre]) pre++;
    let suf = 0;
    while (suf < TA.length - pre && suf < TB.length - pre && TA[TA.length - 1 - suf] === TB[TB.length - 1 - suf]) suf++;
    const A = TA.slice(pre, TA.length - suf), B = TB.slice(pre, TB.length - suf);
    const n = A.length, m = B.length, max = n + m;
    const v = new Int32Array(2 * max + 3), trace = [];
    const off = max + 1;
    let done = max === 0;
    for (let d = 0; d <= max && !done; d++) {
      if (d > MAX_D) return null;
      trace.push(v.slice(off - d - 1, off + d + 2)); // k in [-d-1, d+1] -> index k + d + 1
      for (let k = -d; k <= d; k += 2) {
        let x = (k === -d || (k !== d && v[off + k - 1] < v[off + k + 1])) ? v[off + k + 1] : v[off + k - 1] + 1;
        let y = x - k;
        while (x < n && y < m && A[x] === B[y]) { x++; y++; }
        v[off + k] = x;
        if (x >= n && y >= m) { done = true; break; }
      }
    }
    const ops = [];
    let x = n, y = m;
    for (let d = trace.length - 1; d >= 0; d--) {
      const vv = trace[d], at = (k) => vv[k + d + 1], k = x - y;
      const prevK = (k === -d || (k !== d && at(k - 1) < at(k + 1))) ? k + 1 : k - 1;
      const px = at(prevK), py = px - prevK;
      while (x > px && y > py) ops.push(["=", A[--x]]), y--;
      if (d > 0) { if (x === px) ops.push(["+", B[--y]]); else ops.push(["-", A[--x]]); }
      x = px; y = py;
    }
    ops.reverse();
    if (pre) ops.unshift(["=", TA.slice(0, pre).join("")]);
    if (suf) ops.push(["=", TA.slice(TA.length - suf).join("")]);
    // Group each change as "all removed, then all added", folding in single spaces
    // that sit between edits so a rewrite reads as one replacement, not confetti.
    const out = [];
    let del = "", ins = "";
    const flush = () => { if (del) out.push(["-", del]); if (ins) out.push(["+", ins]); del = ins = ""; };
    for (let i = 0; i < ops.length; i++) {
      const [op, s] = ops[i];
      if (op === "-") del += s;
      else if (op === "+") ins += s;
      else if ((del || ins) && /^\s+$/.test(s) && !s.includes("\n") && ops[i + 1] && ops[i + 1][0] !== "=") { del += s; ins += s; }
      else {
        flush();
        if (out.length && out[out.length - 1][0] === "=") out[out.length - 1][1] += s; else out.push(["=", s]);
      }
    }
    flush();
    return out;
  }

  // ---- Per-highlight suggestions ----
  // Each option is plain data: replace text[start, end) with `text`. The page applies it.

  function sentenceAround(text, start, end) {
    let s = start;
    while (s > 0 && text[s - 1] !== "\n" && !(/\s/.test(text[s - 1]) && /[.!?]/.test(text[s - 2] || ""))) s--;
    let e = end;
    while (e < text.length && text[e] !== "\n" && !/[.!?]/.test(text[e])) e++;
    while (e < text.length && /[.!?)"'”’]/.test(text[e])) e++;
    // Trim surrounding whitespace off the sentence itself.
    while (s < e && /\s/.test(text[s])) s++;
    while (e > s && /\s/.test(text[e - 1])) e--;
    return [s, e];
  }

  // When deleting, also take the space after it (and the line break, if the line empties).
  function widenDeletion(text, start, end) {
    while (end < text.length && /[ \t]/.test(text[end])) end++;
    const lineStart = start === 0 || text[start - 1] === "\n";
    if (lineStart && text[end] === "\n") end++;
    else if (end === text.length) while (start > 0 && /[ \t]/.test(text[start - 1])) start--;
    return [start, end];
  }

  const THREE = /^(.+?), (.+?),? and (.+)$/i;
  const FUNC = new Set(("that this these those my our your their his her its of in on at for to with by from " +
    "about into over every each both all and or but as is are was were be been").split(" "));

  function suggest(text, hit, opts) {
    const out = [];
    const span = text.slice(hit.start, hit.end);
    const op = (start, end, rep, label, kind) => {
      if (rep === "") [start, end] = widenDeletion(text, start, end);
      out.push({ start, end, text: rep, label, kind: kind || "replace", before: text.slice(start, end) });
    };

    // Placeholders: the writer types the real value.
    if (hit.pattern === "placeholder") {
      out.push({ kind: "fill", start: hit.start, end: hit.end, before: span, label: "Fill in" });
      return out;
    }

    // Lists of three: let the writer pick which two to keep.
    if (hit.pattern === "rule of three") {
      const m = span.match(THREE);
      if (m) {
        let [a, b, c] = [m[1], m[2], m[3]], pre = "", post = "";
        // The scanner's item can swallow a neighbouring function word ("that consistency",
        // "leadership at"). Keep those outside the list so dropping an item stays grammatical.
        const fa = a.match(/^(\S+) (.+)$/);
        if (fa && FUNC.has(fa[1].toLowerCase())) { pre = fa[1] + " "; a = fa[2]; }
        const fc = c.match(/^(.+) (\S+)$/);
        if (fc && FUNC.has(fc[2].toLowerCase())) { post = " " + fc[2]; c = fc[1]; }
        const endsClean = !!post || hit.end >= text.length || /^\s*([.!?,;:\n]|$)/.test(text.slice(hit.end, hit.end + 2));
        const keep = (x, y) => op(hit.start, hit.end, `${pre}${x} and ${y}${post}`, `Keep “${x} and ${y}”`);
        // The scanner only sees up to two words per item, so the first and last items may be
        // cut off ("supply [chain operations]"). Dropping the middle one is always safe; the
        // ends only when they're clearly whole.
        if (!/ /.test(a)) keep(b, c);
        keep(a, c);
        if (endsClean) keep(a, b);
      }
      return out;
    }

    // Single words: swap just the word when we have a plain alternative.
    if (hit.category === "language") {
      let w = span;
      for (const [rx, to] of wordRules) w = w.replace(rx, (m) => matchCase(m, to));
      if (w !== span) { op(hit.start, hit.end, w, w ? `Replace with “${w}”` : `Delete “${span}”`); return out; }
    }

    // Otherwise rewrite the sentence with the safe fixes, if that changes it.
    const [s, e] = sentenceAround(text, hit.start, hit.end);
    const sentence = text.slice(s, e);
    const fixed = fix(sentence, opts);
    // Only offer it if the rewrite actually removes what was flagged.
    const norm = (x) => x.toLowerCase().replace(/\s+/g, " ");
    if (fixed !== sentence && !norm(fixed).includes(norm(span).trim())) op(s, e, fixed, fixed ? "Rewrite sentence" : "Delete sentence");
    return out;
  }

  const api = { fix, diff, suggest };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.UnbotFix = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
