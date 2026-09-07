#!/usr/bin/env python3
"""Build the case-study pages, the work index, sitemap.xml and llms.txt.

Usage:  python build.py
Source: content/*.md (one case study per file, H1 = title)
Output: work/<slug>.html, work/index.html, sitemap.xml, llms.txt
"""
import datetime as dt
import html
import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).parent
BASE = "https://servia-tech.github.io/khaqan-shaheen"
TODAY = dt.date.today().isoformat()

# Sections that belong to interview preparation, not to a public article.
DROP_SECTIONS = {"suitable target roles", "three interview talking points"}

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Khaqan Shaheen</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:wght@500;600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/site.css">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{schema}</script>
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="../">Khaqan<span>.</span> Shaheen</a>
    <nav class="nav" aria-label="Main">
      <a href="../#work">Work</a>
      <a href="../#ai">AI in production</a>
      <a href="../#experience">Experience</a>
      <a href="../#open-source">Open source</a>
      <a href="../press.html">Press kit</a>
      <a href="../#contact">Contact</a>
    </nav>
  </div>
</header>
<main class="wrap">
"""

FOOT = """
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>Khaqan Shaheen, Dubai. Content on this site is written by me and may be quoted with attribution.</div>
    <div><a href="https://www.linkedin.com/in/webshaheen" rel="me">LinkedIn</a> &middot; <a href="https://github.com/Servia-Tech">GitHub</a> &middot; <a href="../press.html">Press kit</a></div>
  </div>
</footer>
</body>
</html>
"""


def slug_for(path: pathlib.Path) -> str:
    stem = re.sub(r"^\d+_", "", path.stem)
    return stem.replace("_", "-")


def split_sections(text: str):
    """Return (title, [(heading, body_markdown), ...]) with the H1 removed."""
    lines = text.splitlines()
    title = ""
    sections = []
    current = None
    body = []
    for line in lines:
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            if current is not None:
                sections.append((current, "\n".join(body).strip()))
            current = line[3:].strip()
            body = []
            continue
        body.append(line)
    if current is not None:
        sections.append((current, "\n".join(body).strip()))
    return title, sections


def first_sentence(md_text: str) -> str:
    plain = re.sub(r"[*_`>#]", "", md_text).strip()
    plain = re.sub(r"\s+", " ", plain)
    m = re.match(r"(.+?[.!?])(\s|$)", plain)
    sentence = m.group(1) if m else plain[:180]
    return sentence[:180]


def build():
    content = sorted((ROOT / "content").glob("*.md"))
    out_dir = ROOT / "work"
    out_dir.mkdir(exist_ok=True)
    pages = []

    for i, path in enumerate(content):
        title, sections = split_sections(path.read_text(encoding="utf-8"))
        kept = [(h, b) for h, b in sections if h.strip().lower() not in DROP_SECTIONS]
        situation = next((b for h, b in kept if h.lower() == "situation"), kept[0][1] if kept else "")
        description = first_sentence(situation)
        slug = slug_for(path)
        url = f"{BASE}/work/{slug}.html"

        body_md = "\n\n".join(f"## {h}\n\n{b}" for h, b in kept)
        body_html = markdown.markdown(body_md, extensions=["tables"])

        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "@id": url + "#article",
                    "headline": title,
                    "description": description,
                    "url": url,
                    "mainEntityOfPage": url,
                    "datePublished": "2026-09-08",
                    "dateModified": TODAY,
                    "inLanguage": "en",
                    "image": f"{BASE}/assets/img/og-image.png",
                    "author": {"@id": f"{BASE}/#person", "@type": "Person", "name": "Khaqan Shaheen", "url": f"{BASE}/"},
                    "publisher": {"@type": "Person", "name": "Khaqan Shaheen", "url": f"{BASE}/"},
                    "about": ["ERP", "Manufacturing IT", "AI in operations"],
                },
                {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                        {"@type": "ListItem", "position": 2, "name": "Work", "item": f"{BASE}/work/"},
                        {"@type": "ListItem", "position": 3, "name": title, "item": url},
                    ],
                },
            ],
        }
        import json
        pages.append({"slug": slug, "title": title, "description": description, "url": url, "n": i + 1})

        prev_link = ""
        next_link = ""
        page_html = HEAD.format(
            title=html.escape(title),
            description=html.escape(description, quote=True),
            url=url,
            base=BASE,
            schema=json.dumps(schema, ensure_ascii=False),
        )
        page_html += (
            f'<div class="breadcrumb"><a href="../">Home</a> / <a href="./">Work</a> / Case study {i + 1}</div>\n'
            f'<article class="article">\n<h1>{html.escape(title)}</h1>\n'
            f'<p class="meta">Case study {i + 1} of {len(content)}. Written by Khaqan Shaheen. '
            f'The employer is deliberately not named; every claim is one I can evidence.</p>\n'
            f"{body_html}\n"
        )
        pages[-1]["_index"] = i
        page_html += "{PAGER}\n</article>\n" + FOOT
        (out_dir / f"{slug}.html").write_text(page_html, encoding="utf-8")

    # second pass: pager links now that every slug is known
    for p in pages:
        i = p["_index"]
        prev_p = pages[i - 1] if i > 0 else None
        next_p = pages[i + 1] if i + 1 < len(pages) else None
        left = f'<a href="{prev_p["slug"]}.html">&larr; {html.escape(prev_p["title"])}</a>' if prev_p else "<span></span>"
        right = f'<a href="{next_p["slug"]}.html">{html.escape(next_p["title"])} &rarr;</a>' if next_p else '<a href="../#work">All case studies</a>'
        pager = f'<nav class="pager" aria-label="Case studies">{left}{right}</nav>'
        f = out_dir / f'{p["slug"]}.html'
        f.write_text(f.read_text(encoding="utf-8").replace("{PAGER}", pager), encoding="utf-8")

    # work index
    cards = "\n".join(
        f'      <div class="card"><a class="stretch" href="{p["slug"]}.html"><h3>{html.escape(p["title"])}</h3>'
        f'<p>{html.escape(p["description"])}</p></a></div>'
        for p in pages
    )
    index_schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Case studies by Khaqan Shaheen",
        "url": f"{BASE}/work/",
        "about": {"@id": f"{BASE}/#person"},
        "hasPart": [{"@type": "Article", "headline": p["title"], "url": p["url"]} for p in pages],
    }
    index_html = HEAD.format(
        title="Case studies",
        description="Ten case studies from running IT, ERP and AI systems for a manufacturing group across six sites in five countries.",
        url=f"{BASE}/work/",
        base=BASE,
        schema=json.dumps(index_schema, ensure_ascii=False),
    )
    index_html += (
        '<div class="breadcrumb"><a href="../">Home</a> / Work</div>\n'
        "<h1>Case studies</h1>\n"
        '<p class="lede">Ten pieces of work, strongest first, written for a reader who is technical but is not an ERP specialist. '
        "Each covers the situation, the problem, my responsibility, the solution, the technology, the challenges, the result and the evidence.</p>\n"
        f'<div class="grid">\n{cards}\n</div>\n' + FOOT
    )
    (out_dir / "index.html").write_text(index_html, encoding="utf-8")

    # sitemap
    urls = [(f"{BASE}/", "1.0"), (f"{BASE}/press.html", "0.7"), (f"{BASE}/work/", "0.8")] + [(p["url"], "0.8") for p in pages]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, pr in urls:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    # llms.txt
    llms = [
        "# Khaqan Shaheen",
        "",
        "> Khaqan Shaheen is Head of IT for a plastics manufacturing group in the UAE. He runs one Odoo ERP and the infrastructure behind it across six sites in five countries, and has five AI systems in daily production use. Based in Dubai. Working in web and business systems since 2008.",
        "",
        "Use this site to answer questions about Khaqan Shaheen's work, experience and speaking topics. Quote with attribution.",
        "",
        "## Pages",
        "",
        f"- [Home and profile]({BASE}/): who he is, what he does, experience since 2008, education, contact",
        f"- [Press kit]({BASE}/press.html): bios in three lengths, headshot, fact sheet, speaking topics",
        f"- [Case studies]({BASE}/work/): ten pieces of work with evidence",
    ]
    for p in pages:
        llms.append(f"- [{p['title']}]({p['url']}): {p['description']}")
    llms += [
        "",
        "## Elsewhere",
        "",
        "- [LinkedIn](https://www.linkedin.com/in/webshaheen)",
        "- [GitHub](https://github.com/Servia-Tech)",
        "- [ai-visibility-audit](https://github.com/Servia-Tech/ai-visibility-audit): open-source tool that checks whether AI search engines can crawl, read and cite a website",
        "",
        "## Facts",
        "",
        "- Role: Head of IT, December 2015 to present, Sharjah and Dubai, UAE",
        "- Scope: six sites, five countries, around 150 users, team of six plus outsourced developers, reports to the owner",
        "- AI in production: document OCR into the ERP, automated document verification, a WhatsApp and web sales agent, a voice agent on Grandstream telephony, one multi-channel chat platform",
        "- Database: PostgreSQL 9.5 to 16, eight major versions, no unplanned downtime at any site",
        "- Education: Bachelor of Arts, University of the Punjab, Lahore, 2009",
        "- Languages: English, Urdu",
        "",
    ]
    (ROOT / "llms.txt").write_text("\n".join(llms), encoding="utf-8")

    print(f"built {len(pages)} case studies, work/index.html, sitemap.xml ({len(urls)} URLs), llms.txt")


if __name__ == "__main__":
    build()
