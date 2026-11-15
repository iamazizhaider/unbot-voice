# unbot-voice

Find and fix what makes writing sound like AI.

- **Playground:** paste a draft and see the giveaways highlighted, each with a fix. The Fixed tab applies the mechanical fixes for you and shows what's left. [Try it in your browser](https://iamazizhaider.github.io/unbot-voice/). Nothing you paste is uploaded.
- **Claude skill:** rewrites drafts, audits them, or writes in your own voice.

## What it does

**Before** (scores 194 tells per 1,000 words)
> I almost didn't post this. But here's the thing: after 10 years in marketing, I've learned that success isn't about working harder — it's about working smarter. Last quarter, our team faced a pivotal moment. [...] The result? A 40% increase in qualified leads. No fancy tools. No massive budget. Just a relentless focus on our customers.

**After** (scores 0)
> Last quarter our lead numbers were flat for the third quarter running, so we stopped running paid campaigns for six weeks and called customers instead. About 30 of them. Most said the same thing: our landing pages explained features they didn't care about and skipped the one question they all had, which was whether it worked with their existing CRM. We rewrote three pages around that answer. Qualified leads went up 40% the following quarter. Same budget, same tools.

AI text tends to replace specific facts with generic significance ("a pivotal moment", "a relentless focus"). The skill puts the facts back. When it doesn't have them, it asks you instead of making them up. More examples are in [examples.md](skills/unbot-voice/references/examples.md).

## Install

**Claude Code plugin**

```
/plugin marketplace add iamazizhaider/unbot-voice
/plugin install unbot-voice@unbot-voice
```

**Claude Code personal skill** (gives you the short `/unbot-voice` command)

```bash
git clone https://github.com/iamazizhaider/unbot-voice.git
cp -r unbot-voice/skills/unbot-voice ~/.claude/skills/
```

**Claude.ai and the desktop app:** download `unbot-voice.zip` from the [latest release](https://github.com/iamazizhaider/unbot-voice/releases/latest), then upload it in **Settings → Capabilities → Skills**.

## Usage

| You say | What happens |
|---|---|
| `/unbot-voice` + pasted text, or "humanize this" | **Rewrite**: a revised version, the main changes, and before/after scores |
| "Does this sound like AI?" | **Audit**: each tell, quoted, with a fix. Nothing is changed. |
| "Write a LinkedIn post about X" | **Write**: a draft in a natural voice |
| "Here are three things I wrote, learn my voice" | **Voice profile**: your style, written down so later drafts match it |

The skill adjusts to the venue. A spec stays structured, an encyclopedia entry stays neutral, and a LinkedIn post loses the drama.

The scanner also runs from the command line, with no install needed:

```bash
python3 skills/unbot-voice/scripts/scan.py draft.md
```

| Score | Reading |
|---|---|
| under 10 | few tells |
| 10–25 | some tells, worth a pass |
| 25–50 | reads as AI-assisted |
| 50+ | reads as unedited AI output |

## What it looks for

The full catalog is in [patterns.md](skills/unbot-voice/references/patterns.md). The main groups:

- **Chatbot residue:** "I hope this helps", "As an AI", "[Your Name]", `utm_source=chatgpt.com`.
- **Forced voice:** "Here's the thing:", "The result?", "In today's fast-paced digital landscape".
- **Content:** inflated significance ("plays a pivotal role", "a testament to"), weasel attributions ("experts argue"), and "despite these challenges" endings.
- **Language:** vocabulary by model era (*delve, tapestry* in 2023; *showcasing, fostering* in 2024–25; *leverage, quietly, steady* in 2026), "serves as" instead of "is", and "it's not X, it's Y".
- **Style:** em-dash habits, uniform sentence length, emoji bullets, "In conclusion".

On eight typical AI drafts (in [evals/](evals/)), scores went from 173–277 before rewriting to 0–5 after. The opening of Thoreau's *Walden* (1854) scores 8, which shows it doesn't just flag long or formal sentences.

## Limitations

- **It isn't an AI detector.** These signs are evidence, not proof. People write like this too, which is where models picked it up.
- **It isn't a detector-evasion tool.** If you're submitting somewhere that requires AI disclosure (a course, a journal, Wikipedia), the skill will improve the writing and remind you of the policy.
- **The scanner only sees patterns.** It can't tell when a sentence is generic but uses no flagged words. The skill reads for that. The scanner doesn't.
- **The tells go out of date.** The catalog is dated, and [patterns.md](skills/unbot-voice/references/patterns.md#keeping-this-current) explains how to refresh it.

## Credits

Inspired by [blader/humanizer](https://github.com/blader/humanizer), the original Claude skill for removing signs of AI writing. If you're choosing between them, try both. unbot-voice adds the browser playground, the scanner score, voice profiles and venue-specific guidance.

The patterns come from Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide and Hunting the Muse's [How to tell if writing is AI](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai).

## License

MIT, except `skills/unbot-voice/references/patterns.md`, which adapts material from Wikipedia and is CC BY-SA 4.0. See [LICENSE](LICENSE).
