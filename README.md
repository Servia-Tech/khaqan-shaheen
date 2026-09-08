# khaqanshaheen

Source for the personal site of Khaqan Shaheen, Head of IT in Dubai. Static HTML, no framework, served by GitHub Pages.

Live website: [khaqanshaheen.com](https://khaqanshaheen.com/).

- `index.html`, `press.html`: hand-written pages
- `content/*.md`: the ten case studies, one Markdown file each
- `build.py`: renders `content/` into `work/`, and writes `sitemap.xml` and `llms.txt`
- `assets/`: stylesheet and images

Rebuild after editing a case study:

```
python -m pip install markdown
python build.py
```

Text and images are copyright Khaqan Shaheen. Quote with attribution.

For articles, tutorials and notes, keep the original `date` in the Markdown front matter. Add `modified: YYYY-MM-DD` when the content materially changes. Rebuilding the site alone must not advance an article's modification date. The same date is used in its structured data and sitemap.
