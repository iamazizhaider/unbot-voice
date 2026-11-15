#!/usr/bin/env python3
"""unbot-voice scanner: flag common signs of AI-generated writing.

Usage:
    python3 scan.py FILE [FILE ...]
    cat draft.txt | python3 scan.py
    python3 scan.py docs/*.md --threshold 25          # exit 1 if any file scores above 25
    python3 scan.py README.md --format github         # GitHub Actions annotations
    python3 scan.py draft.md --json

Standard library only. Patterns live in patterns.json next to this file and
are shared with the browser playground. They come from Wikipedia's "Signs of
AI writing" guide and Hunting the Muse's "How to tell if writing is AI".
A high score is evidence, not proof: humans write like this too.
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "patterns.json"), encoding="utf-8") as fh:
    _DATA = json.load(fh)
COMPILED = [(p["category"], p["label"], re.compile(p["regex"], re.IGNORECASE | re.MULTILINE), p["weight"], p.get("tip", ""))
            for p in _DATA["patterns"]]

CATEGORIES = ("residue", "forced-voice", "content", "language", "style")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
# Short quoted spans are usually mentions ("words like 'delve'"), not use.
QUOTED = re.compile(r"\"[^\"\n]{1,80}\"|“[^”\n]{1,80}”|`[^`\n]{1,80}`")
CODE_FENCE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)


def mask(text, include_quotes=False):
    """Blank out code blocks (and short quotes) while keeping offsets and line numbers."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    text = CODE_FENCE.sub(blank, text)
    if not include_quotes:
        text = QUOTED.sub(blank, text)
    return text


def sentence_lengths(text):
    prose = re.sub(r"(^|\n)\s*([-*#>|]|\d+\.)\s.*", "", text)  # drop list, heading, table lines
    sents = [s for s in SENT_SPLIT.split(prose.strip()) if len(s.split()) >= 3]
    return [len(s.split()) for s in sents]


def band(score):
    if score < 10:
        return "low: few tells"
    if score < 25:
        return "moderate: some tells, worth a pass"
    if score < 50:
        return "high: reads as AI-assisted"
    return "very high: reads as unedited AI output"


def scan(text, include_quotes=False):
    scanned = mask(text, include_quotes)
    words = len(re.findall(r"\b\w+\b", scanned))
    hits = []
    for cat, label, rx, weight, tip in COMPILED:
        for m in rx.finditer(scanned):
            if not m.group(0).strip():
                continue
            line = scanned.count("\n", 0, m.start()) + 1
            hits.append({"category": cat, "pattern": label, "match": " ".join(m.group(0).split()),
                         "line": line, "weight": weight, "tip": tip})

    em = scanned.count("—") + len(re.findall(r"\s--\s", scanned))
    lengths = sentence_lengths(scanned)
    stats = {"words": words, "sentences": len(lengths), "em_dashes": em}
    rhythm_flag = None
    if len(lengths) >= 5:
        mean, sd = statistics.mean(lengths), statistics.pstdev(lengths)
        stats.update(mean_sentence_len=round(mean, 1), sentence_len_stdev=round(sd, 1))
        if sd / mean < 0.35:
            rhythm_flag = f"uniform sentence length (stdev {sd:.1f} vs mean {mean:.1f}); vary the rhythm"

    per_k = 1000 / max(words, 1)
    em_rate = em * per_k
    em_flag = f"{em} em dashes ({em_rate:.1f} per 1,000 words)" if em >= 2 and em_rate > 4 else None

    score = sum(h["weight"] for h in hits) * per_k
    if em_flag:
        score += min(em_rate, 15)
    if rhythm_flag:
        score += 5
    score = round(score, 1)
    return {"score": score, "band": band(score), "stats": stats,
            "flags": [f for f in (em_flag, rhythm_flag) if f], "hits": hits}


def report_text(name, r):
    out = [f"== {name} ==",
           f"AI-tell score: {r['score']} per 1,000 words ({r['band']})",
           "Stats: " + ", ".join(f"{k}={v}" for k, v in r["stats"].items())]
    out += [f"! {f}" for f in r["flags"]]
    if not r["hits"]:
        out.append("No pattern hits.")
    for cat in CATEGORIES:
        hs = [h for h in r["hits"] if h["category"] == cat]
        if hs:
            out.append(f"\n[{cat}]")
            for h in sorted(hs, key=lambda h: (-h["weight"], h["line"])):
                out.append(f"  L{h['line']:<4} {h['pattern']:<32} \"{h['match']}\"")
    return "\n".join(out)


def report_github(name, r, threshold):
    out = []
    for h in r["hits"]:
        level = "warning" if h["weight"] >= 2 else "notice"
        out.append(f"::{level} file={name},line={h['line']},title=unbot-voice: {h['pattern']}::\"{h['match']}\"")
    over = threshold is not None and r["score"] > threshold
    level = "error" if over else "notice"
    out.append(f"::{level} file={name},title=unbot-voice score {r['score']}::{r['band']}"
               + (f" (threshold {threshold})" if threshold is not None else ""))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Flag common signs of AI writing.")
    ap.add_argument("files", nargs="*", help="files to scan (default: stdin)")
    ap.add_argument("--json", action="store_true", help="output JSON")
    ap.add_argument("--format", choices=("text", "github"), default="text", help="output format")
    ap.add_argument("--threshold", type=float, help="exit 1 if any file scores above this")
    ap.add_argument("--min-words", type=int, default=50,
                    help="skip threshold check for files shorter than this (default 50)")
    ap.add_argument("--include-quotes", action="store_true",
                    help="also scan text inside short quotes and inline code")
    args = ap.parse_args(argv)

    if args.files:
        inputs = []
        for f in args.files:
            with open(f, encoding="utf-8", errors="replace") as fh:
                inputs.append((f, fh.read()))
    else:
        inputs = [("stdin", sys.stdin.read())]
    results = {name: scan(text, args.include_quotes) for name, text in inputs}

    if args.json:
        print(json.dumps(results if len(results) > 1 else next(iter(results.values())), indent=2))
    elif args.format == "github":
        print("\n".join(report_github(n, r, args.threshold) for n, r in results.items()))
    else:
        print("\n\n".join(report_text(n, r) for n, r in results.items()))
        print("\nNote: this flags patterns, it doesn't prove authorship. Judge each hit in context.")

    if args.threshold is not None:
        failing = [n for n, r in results.items()
                   if r["score"] > args.threshold and r["stats"]["words"] >= args.min_words]
        if failing:
            print(f"\nunbot-voice: {len(failing)} file(s) above threshold {args.threshold}: {', '.join(failing)}",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
