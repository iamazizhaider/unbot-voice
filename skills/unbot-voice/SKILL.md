---
name: unbot-voice
description: Rewrite or write prose so it reads like a person wrote it, not a chatbot. Use when the user runs /unbot-voice, asks to "humanize" text, make writing sound less like AI, remove AI tells, de-slop a draft, match their own voice, or check whether text reads as AI-generated. Also use when drafting posts, emails, articles, bios, or essays where the user wants a natural human voice. Works on pasted text, files, or Claude's own drafts.
---

# unbot-voice

Make writing sound like a specific person with something to say, not a model averaging over the internet.

**Bundled files** (paths relative to this skill's directory):
- `references/patterns.md`: the full catalog of AI tells, by category and model era. Read it before the first rewrite in a session.
- `references/venues.md`: what to fix and what to keep for LinkedIn, email, blogs, academic, encyclopedic, docs, marketing and fiction. Read the section for the current venue.
- `references/examples.md`: six worked before/after rewrites. Skim it to calibrate.
- `scripts/scan.py`: a pattern scanner that flags tells with line numbers, a fix tip for each, and a score per 1,000 words. It reads its rules from `scripts/patterns.json` and needs only the Python standard library. Text inside short quotes and code blocks counts as a mention and is skipped (`--include-quotes` overrides this).

Catalog last updated November 2026, from Wikipedia's "Signs of AI writing" guide and Hunting the Muse's "How to tell if writing is AI".

## The core idea

AI text "regresses to the mean." Specific facts get swapped for generic significance ("invented the first train-coupling device" turns into "a revolutionary titan of industry"). Plain verbs get replaced with inflated ones, and every paragraph reaches for a lesson. Swapping banned words for synonyms doesn't fix this. The fix is to put back what a real writer has: specifics, a point of view, uneven rhythm, and the nerve to just say the thing.

Surface tells are symptoms. If you only scrub vocabulary, the text still reads as AI, and now it's harder to spot. Fix the substance first.

## Modes

Work out which one the user wants. If it's unclear, ask once.

1. **Rewrite** (default): the user gives you text and you return a humanized version.
2. **Audit**: you report the tells you found and change nothing. Use this for "does this sound like AI?"
3. **Write**: you draft new content from scratch, applying everything below.
4. **Voice profile**: the user shares samples of their own writing and you build a profile to write in (see below).

## Workflow

### 1. Get context
Find out who the writer is, who reads it, where it goes and what voice they want. Then read the matching section of `references/venues.md`. If the user has a voice profile (see "Voice matching"), use it. Otherwise pick a voice that fits the venue and say which one you picked.

### 2. Scan
If the text is in a file, or long enough to be worth it, run the scanner:

```bash
python3 <skill-dir>/scripts/scan.py draft.txt        # or: pbpaste | python3 .../scan.py
```

The scanner catches vocabulary, phrase templates, em-dash density, uniform sentence rhythm and chatbot residue. It **cannot** catch the deeper problems: generic claims with no fact behind them, elegant variation, a missing point of view, or meaning that drifted. Read for those yourself against `references/patterns.md`. Weight density over single hits. One "crucial" is fine, but four AI words in a paragraph is a tell. Treat each hit as a question, not a verdict, because "highlighting" can be literal.

### 3. Rewrite
Apply these, roughly in priority order:

1. **Specifics over significance.** Replace "plays a pivotal role in" with what it actually does. If you don't have the concrete fact, **ask the user for it**, or cut the claim, or leave a marked gap like `[which project?]`. Never invent names, numbers, dates, quotes or anecdotes. (See example 4 in `references/examples.md`.)
2. **Delete the scaffolding.** Cut "It's important to note that", "In conclusion", "Overall", throat-clearing intros, recap closers and "Despite these challenges..." paragraphs. Start where the content starts and stop when it's done.
3. **Use plain verbs and "is".** Write "is" rather than "serves as" or "stands as", "has" rather than "boasts" or "features", "uses" rather than "leverages", "wrote" rather than "authored", "help" rather than "foster".
4. **Break the formulas.**
   - Rule of three: keep a list of three only when all three items earn their place. Two is fine. One is often better.
   - "Not X, but Y", "It's not just X, it's Y" and "No X. No Y. Just Z.": say Y directly.
   - "X rather than Y" and "On one hand... on the other": drop the straw man and take a position, if the genre allows one.
   - Trailing "-ing" clauses ("..., highlighting its importance"): delete them, or make them a real sentence with a source.
5. **Vary the rhythm on purpose.** Mix short sentences with long ones. Let one run on a bit. Fragments are fine sometimes. The exception is encyclopedic text, where uniformity is normal.
6. **Fix punctuation without overcorrecting.** Replace most em dashes with commas, periods, parentheses or colons. Keep one if it's genuinely the best mark. Don't strip all varied punctuation, because uniformly flat punctuation is a newer tell.
7. **Turn formatting back into prose** unless the venue needs structure. Drop bold mid-sentence, emoji headers and "**Label:** text" bullet lists. Use sentence-case headings.
8. **Attribute or cut.** Replace "Experts argue" or "Industry reports suggest" with a named source, or delete the line.
9. **Allow a point of view.** Use selective hedges ("probably", "I think"), committed superlatives the writer believes, and contractions where the register allows them.
10. **Repeat words when they're the right words.** Call the subject the same thing every time instead of rotating synonyms.
11. **Strip chatbot residue completely.** That includes pleasantries, offers to do more, disclaimers about training, placeholders and stray markdown.

### 4. Self-audit
Run the scanner again on your output and reread it. Check specifically for:
- tells you introduced while rewriting (2026-era words like "quietly", "steady", "practical" and "matters" sneak in easily)
- any sentence you could paste into a thousand other articles unchanged, which you should make specific or cut
- whether you kept the original meaning and every real fact, and **added no new facts**

A low scanner score is necessary but not enough. Text can score 0 and still be generic.

### 5. Return
- **Rewrite mode:** give the revised text first, then up to five short bullets naming the biggest changes, plus the before and after scores if you ran the scanner. List any claims you cut for lacking a fact, so the user can supply one.
- **Audit mode:** for each tell, give the quoted span, the pattern name and a suggested fix, grouped by category. Then give an overall verdict and its reasoning. Never claim certainty: detectors and human judges both have high error rates.
- **Write mode:** give the draft only, unless the user asks for commentary.

## Voice matching

When the user shares 2–3 samples of their own writing (ideally 300+ words in total, written before 2023 or definitely by them), pull out a short profile:

- **Sentence length:** the typical range, and whether they use fragments or run-ons
- **Register:** contractions, profanity, slang, how formal they are
- **Punctuation habits:** semicolons, parentheses, dashes, exclamation marks, ellipses
- **Openings and endings:** how they start (a claim, a scene, a question?) and whether they wrap up or just stop
- **Quirks:** recurring phrases, humor style, how they hedge, pet words
- **Things they never do**

Show the profile to the user as 6–10 bullets. Offer to save it, for example as `voice.md` in their project, or in memory if that's available, so later sessions can reuse it. When you write in their voice, keep their habits even if the catalog flags them. If they really do use em dashes, keep their em dashes.

## Guardrails

- **Don't fabricate.** Humanizing never means inventing anecdotes, quotes, numbers or "I remember when..." stories. Ask, cut, or mark the gap.
- **Don't help pass off AI text where disclosure is required.** That covers academic work under an AI policy, Wikipedia (which restricts LLM content), and contests or publications that ban AI. Improve the writing, but name the policy. Polishing your own drafts and text you'll stand behind is fine.
- **This isn't a detector-evasion tool.** The goal is better writing. Lower detector scores are a side effect.
- **Respect the genre.** Specs stay structured and encyclopedic text stays neutral.
- **Keep the user's voice over yours.**
