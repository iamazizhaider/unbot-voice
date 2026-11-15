# Evals

`before/` holds eight typical AI drafts (LinkedIn, blog intro, cold email, bio, encyclopedia paragraph, product copy, essay, status update). `after/` holds a humanized rewrite of each, made by following `SKILL.md`.

The specific facts in the rewrites (names, numbers, dates) are illustrative. In real use they come from the user. The skill never invents them.

Run from the repo root:

```bash
python3 skills/unbot-voice/scripts/scan.py evals/before/*.txt evals/after/*.txt
```

Results at release (tells per 1,000 words):

| Sample | Before | After |
|---|---:|---:|
| 01 LinkedIn post | 194 | 0 |
| 02 Blog intro | 203 | 0 |
| 03 Cold email | 212 | 0 |
| 04 Bio | 193 | 0 |
| 05 Encyclopedia paragraph | 277 | 5 |
| 06 Product copy | 173 | 0 |
| 07 Essay | 197 | 0 |
| 08 Status update | 184 | 0 |

For a false-positive check, the opening of Thoreau's *Walden* (1854) scores 8, in the "low" band.

A low score is necessary, not sufficient. The scanner can't tell whether a rewrite kept the meaning or whether it's still generic, so read the outputs too.
