"""Build the static pages GitHub Pages serves next to the playground.

Writes:
  signs-of-ai-writing/index.html  the pattern catalog (patterns.md) as a crawlable guide page
  sitemap.xml                     for Google Search Console and Bing Webmaster Tools
  llms.txt                        a plain-text map of the project for AI answer engines

Run from anywhere:  python3 tools/build_site.py
Check only:         python3 tools/build_site.py --check   (exit 1 if a file is out of date)
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://iamazizhaider.github.io/unbot-voice/"
REPO = "https://github.com/iamazizhaider/unbot-voice"
CATALOG = os.path.join(ROOT, "skills", "unbot-voice", "references", "patterns.md")
PATTERNS = os.path.join(ROOT, "skills", "unbot-voice", "scripts", "patterns.json")


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def inline(text):
    """Escape, then apply the small subset of inline markdown patterns.md uses."""
    codes = []

    def keep_code(m):
        codes.append("<code>" + html.escape(m.group(1)) + "</code>")
        return "\x00%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)

    def link(m):
        href = m.group(2)
        if href.startswith("#"):
            href = "#" + slug(href[1:])
        elif not re.match(r"https?://", href):
            href = REPO + "/blob/main/skills/unbot-voice/references/" + href
        return '<a href="%s">%s</a>' % (html.escape(href), m.group(1))

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def render_catalog(md):
    """Turn patterns.md into HTML sections. Returns (body_html, toc[(id, title)])."""
    lines = md.split("\n")
    # Drop the title block (H1, date, sources); the page writes its own intro.
    start = next(i for i, l in enumerate(lines) if l.startswith("## "))
    out, toc, para, lst = [], [], [], None

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if lst:
            tag = lst[0]
            out.append("<%s>%s</%s>" % (tag, "".join("<li>" + inline(i) + "</li>" for i in lst[1]), tag))
            lst = None

    for line in lines[start:]:
        if line.startswith("## Keeping this current"):
            break  # maintainer notes; they live in the repo
        s = line.strip()
        m = re.match(r"(#{2,3}) (.+)", s)
        if m:
            flush()
            title = re.sub(r"^\d+\.\s*", "", m.group(2))
            level = len(m.group(1))
            hid = slug(title)
            if level == 2:
                toc.append((hid, title))
            out.append('<h%d id="%s">%s</h%d>' % (level, hid, inline(title), level))
        elif s == "---":
            flush()
        elif re.match(r"[-*] ", s) or re.match(r"\d+\. ", s):
            if para:
                flush()
            tag = "ol" if s[0].isdigit() else "ul"
            if lst is None or lst[0] != tag:
                flush()
                lst = (tag, [])
            lst[1].append(re.sub(r"^([-*]|\d+\.) ", "", s))
        elif not s:
            flush()
        else:
            if lst:
                flush()
            para.append(s)
    flush()
    return "\n".join(out), toc


STYLE = """
:root { --bg:#f7f6f3; --surface:#fff; --surface-2:#f1efea; --text:#1b1a17; --muted:#6b675f; --border:#e3e0d8; --focus:#2f5bd3; --accent:#c2410c; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#121211; --surface:#1b1b19; --surface-2:#232320; --text:#ecebe6; --muted:#a29e94; --border:#2f2e2a; --focus:#7aa2ff; --accent:#fb923c; } }
:root[data-theme="dark"] { --bg:#121211; --surface:#1b1b19; --surface-2:#232320; --text:#ecebe6; --muted:#a29e94; --border:#2f2e2a; --focus:#7aa2ff; --accent:#fb923c; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin:0; background:var(--bg); color:var(--text); font:17px/1.65 ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
a { color: inherit; text-underline-offset: 3px; }
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.wrap { max-width: 760px; margin: 0 auto; padding: 0 max(16px, env(safe-area-inset-right)) 48px max(16px, env(safe-area-inset-left)); }
header.top { display:flex; align-items:center; justify-content:space-between; padding:20px 0 8px; gap:12px; }
.brand { display:flex; align-items:center; gap:10px; font-weight:700; font-size:18px; text-decoration:none; }
.brand-mark { width:28px; height:28px; border-radius:7px; background:var(--text); color:var(--bg); display:grid; place-items:center; }
.ghost { border:1px solid var(--border); border-radius:8px; padding:6px 10px; font-size:14px; text-decoration:none; }
.ghost:hover { background: var(--surface-2); }
h1 { font-size: clamp(30px, 5vw, 44px); line-height:1.1; letter-spacing:-.025em; margin:28px 0 12px; }
h2 { font-size: 26px; letter-spacing:-.015em; margin: 44px 0 8px; padding-top: 20px; border-top: 1px solid var(--border); }
h3 { font-size: 19px; margin: 28px 0 4px; }
p, li { overflow-wrap: anywhere; }
.lede { font-size: 19px; color: var(--muted); }
.answer { background: var(--surface); border:1px solid var(--border); border-radius:14px; padding: 16px 20px; margin: 20px 0; }
.answer p { margin: 0 0 8px; } .answer ol { margin: 0 0 10px; padding-left: 22px; }
.cta { display:inline-block; background:var(--text); color:var(--bg); border-radius:10px; padding:10px 16px; font-weight:600; text-decoration:none; margin: 4px 0 8px; }
nav.toc { font-size: 15px; color: var(--muted); }
nav.toc ol { padding-left: 22px; margin: 6px 0 0; }
code { font: 14px ui-monospace,SFMono-Regular,Menlo,monospace; background: var(--surface-2); padding: 1px 5px; border-radius: 5px; }
em { font-style: italic; }
@media (max-width: 360px) { header.top { gap: 8px; } .brand { font-size: 16px; gap: 8px; } .ghost { padding: 5px 7px; } }
footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--border); color: var(--muted); font-size: 14px; }
"""

INTRO = """<h1>Signs of AI writing</h1>
<p class="lede">A field guide to the phrases and habits that make text read like it came from ChatGPT, Claude or Gemini, with a fix for each one. Last updated {updated}.</p>
<div class="answer">
<p><strong>The short answer.</strong> The strongest signs of AI writing are:</p>
<ol>
<li>Chatbot leftovers such as "I hope this helps", "[Your Name]" or "As an AI".</li>
<li>Claims of importance in place of facts: "plays a pivotal role", "a testament to".</li>
<li>Stock drama such as "Here's the thing:" and "The result?"</li>
<li>Words that spiked with each model era: "delve" and "tapestry" in 2023, "showcasing" and "fostering" in 2024–25, "quietly" and "steady" in 2026.</li>
<li>"It's not X, it's Y" and lists of exactly three.</li>
<li>Formatting habits: em dashes, emoji bullets, bold labels, and a closing "In conclusion".</li>
</ol>
<p>One sign proves nothing, because people write this way too. A cluster of them is what gives a draft away.</p>
</div>
<p><a class="cta" href="../playground/">Check your own text</a><br><span style="color:var(--muted);font-size:15px">Free and open source. It runs in your browser, so nothing you paste is uploaded.</span></p>
"""


def build_guide():
    md = open(CATALOG, encoding="utf-8").read()
    updated = re.search(r"\*\*Last updated: ([^.*]+)\.?\*\*", md).group(1).strip()
    body, toc = render_catalog(md)
    n = len(json.load(open(PATTERNS, encoding="utf-8"))["patterns"])
    url = SITE + "signs-of-ai-writing/"
    title = "Signs of AI writing: how to spot it and how to fix it"
    desc = ("A field guide to the signs of AI-generated writing: stock phrases, inflated significance, "
            "AI vocabulary by year, em dashes and chatbot leftovers, with a fix for each. "
            "Includes a free checker that flags %d patterns in your own text." % n)
    ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": title,
        "description": desc,
        "url": url,
        "image": SITE + "assets/og.png",
        "inLanguage": "en",
        "author": {"@type": "Person", "name": "iamazizhaider", "url": "https://github.com/iamazizhaider"},
        "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        "isBasedOn": ["https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing",
                      "https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai"],
        "about": "Signs of AI-generated writing",
    }
    toc_html = "".join('<li><a href="#%s">%s</a></li>' % (i, inline(t)) for i, t in toc)
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#f7f6f3">
<meta property="og:type" content="article">
<meta property="og:site_name" content="unbot-voice">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="unbot-voice: find and fix what makes writing sound like AI">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%23161616'/><path d='M9 10v7a7 7 0 0 0 14 0v-7' stroke='%23fff' stroke-width='3.2' fill='none' stroke-linecap='round'/></svg>">
<script type="application/ld+json">{ld}</script>
<style>{style}</style>
</head>
<body>
<div class="wrap">
<header class="top">
  <a class="brand" href="../playground/"><span class="brand-mark" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 32 32"><path d="M8 7v10a8 8 0 0 0 16 0V7" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round"/></svg></span>unbot-voice</a>
  <nav style="display:flex;gap:6px"><a class="ghost" href="../playground/">Playground</a><a class="ghost" href="{repo}">GitHub</a></nav>
</header>
<main>
<article>
{intro}
<nav class="toc" aria-label="Contents"><strong>Contents</strong><ol>{toc}</ol></nav>
{body}
</article>
</main>
<footer>
<p>Adapted from Wikipedia's <a href="https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing">Signs of AI writing</a> and Hunting the Muse's <a href="https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai">How to tell if writing is AI</a>. This page is licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. The source is <a href="{repo}/blob/main/skills/unbot-voice/references/patterns.md">patterns.md</a> on GitHub.</p>
<p><a href="../playground/">Playground</a> · <a href="{repo}">GitHub</a> · <a href="{repo}#install">Install the Claude skill</a></p>
</footer>
</div>
</body>
</html>
""".format(title=html.escape(title), desc=html.escape(desc), url=url, site=SITE, repo=REPO,
           ld=json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"), style=STYLE.strip(),
           intro=INTRO.format(updated=html.escape(updated)), toc=toc_html, body=body)


def build_sitemap():
    urls = [SITE + "playground/", SITE + "signs-of-ai-writing/"]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join("  <url><loc>%s</loc></url>\n" % u for u in urls)
            + "</urlset>\n")


def build_llms():
    return """# unbot-voice

> Free, open-source tool that finds and fixes the signs of AI-generated writing (stock phrases, inflated significance, AI vocabulary by model era, em-dash habits, chatbot leftovers). It is a writing-quality tool, not an AI detector and not a detector-evasion tool.

- [Playground]({site}playground/): paste text in the browser, see each sign highlighted with a fix, apply fixes and copy the result. Nothing is uploaded.
- [Signs of AI writing]({site}signs-of-ai-writing/): the full pattern catalog as a guide, with a fix for each pattern.
- [README]({repo}#readme): install as a Claude Code plugin or Claude skill, use the command-line scanner, or add the GitHub Action to fail CI on AI-sounding docs.
- [Pattern catalog source]({repo}/blob/main/skills/unbot-voice/references/patterns.md) (CC BY-SA 4.0, adapted from Wikipedia's "Signs of AI writing").
- [Scanner patterns]({repo}/blob/main/skills/unbot-voice/scripts/patterns.json): the regex list shared by the CLI, the GitHub Action and the playground.

## How scoring works

The scanner counts weighted matches per 1,000 words. Under 10 means few signs, 10–25 is worth a pass, 25–50 reads as AI-assisted, and 50+ reads as unedited AI output. Typical AI drafts score 170–280. The same drafts score 0–5 after rewriting.
""".format(site=SITE, repo=REPO)


OUTPUTS = {
    os.path.join(ROOT, "signs-of-ai-writing", "index.html"): build_guide,
    os.path.join(ROOT, "sitemap.xml"): build_sitemap,
    os.path.join(ROOT, "llms.txt"): build_llms,
}


def main(check=False):
    stale = []
    for path, fn in OUTPUTS.items():
        content = fn()
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current != content:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)
    if check and stale:
        print("Out of date (run python3 tools/build_site.py): " + ", ".join(stale))
        return 1
    print(("Up to date" if not stale else "Wrote " + ", ".join(stale)))
    return 0


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
