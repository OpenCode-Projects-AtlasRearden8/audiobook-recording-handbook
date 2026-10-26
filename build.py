#!/usr/bin/env python3
"""Build a static HTML site from the markdown files in docs/.

Local-first and dependency-free: uses only the Python standard library,
so it works on any machine with Python 3.9+ installed. Nothing is
downloaded, nothing is uploaded.

Usage:
    python3 build.py            # build site/ from docs/
    python3 build.py --out DIR  # build into DIR instead
    python3 build.py --check    # validate docs and links without writing anything
"""

from __future__ import annotations

import argparse
import datetime
import html
import re
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
DEFAULT_OUT = ROOT / "site"

# ---------------------------------------------------------------------------
# Inline markdown -> HTML
# ---------------------------------------------------------------------------


def _escape(text: str) -> str:
    return html.escape(text, quote=False)


class _Inline:
    """Convert inline markdown to HTML using token placeholders.

    The base text is HTML-escaped FIRST (so created tags survive), then
    inline code and links are stashed as raw fragments, then bold and
    italic pairs are converted on the escaped text. Stashed fragments are
    restored at the end. Nested spans (e.g. italics inside bold) are
    processed on text that is already escaped, so `escape_first == False for
    recursive calls to avoid double-escaping.
    """

    def __init__(self, text: str, escape_first: bool = True) -> None:
        self.tokens: List[str] = []
        self.output = self._run(text, escape_first)

    def _stash(self, fragment: str) -> str:
        self.tokens.append(fragment)
        return f"\x00{len(self.tokens) - 1}\x00"

    def _run(self, text: str, escape_first: bool) -> str:
        if escape_first:
            text = _escape(text)
        # inline code (contents already escaped by the pass above)
        text = re.sub(r"`([^`]+)`", lambda m: self._stash(f"<code>{m.group(1)}</code>"), text)
        # links
        text = re.sub(
            r"\[([^\]]+)\]\(([^)\s]+)\)",
            lambda m: self._stash(self._link(m.group(1), m.group(2))),
            text,
        )
        # bold, then italic (balanced-marker approach keeps nested spans sane)
        # if bold markers are unbalanced, treat every asterisk as literal text
        if text.count("**") % 2 == 0:
            text = self._wrap_pairs(text, "**", "strong", escape_first=False)
            text = self._wrap_pairs(text, "*", "em", escape_first=False)
        # restore stashed markup
        for i, tok in enumerate(self.tokens):
            text = text.replace(f"\x00{i}\x00", tok)
        return text

    def _wrap_pairs(self, text: str, marker: str, tag: str, escape_first: bool) -> str:
        """Convert balanced marker pairs to a simple tag.

        A non-greedy regex approach fails when a pair's content later gets
        tags itself, so instead we split on the marker and toggle tags on
        alternating segments. An unbalanced marker count leaves the text
        as-is (a data bug in a doc should be caught during review, and the
        site build reports leaks in tests).
        """
        parts = text.split(marker)
        if len(parts) % 2 == 0:  # unbalanced pair(s): leave untouched
            return text
        result = parts[0]
        for k in range(1, len(parts), 2):
            result += f"<{tag}>{_Inline(parts[k], escape_first=escape_first).output}</{tag}>"
            result += parts[k + 1]
        return result

    def _link(self, label: str, target: str) -> str:
        label_html = _Inline(label, escape_first=False).output
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target):
            return (
                f'<a href="{html.escape(target, quote=True)}" target="_blank" '
                f'rel="noopener">{label_html}</a>'
            )
        if target.startswith("mailto:"):
            return f'<a href="{html.escape(target, quote=True)}">{label_html}</a>'
        page, anchor = target.split("#", 1) if "#" in target else (target, "")
        if page.endswith(".md"):
            page = _page_name_for_md(page)
        href = page + (f"#{anchor}" if anchor else "")
        return f'<a href="{html.escape(href, quote=True)}">{label_html}</a>'


def _inline(text: str) -> str:
    return _Inline(text).output


def _page_name_for_md(name: str) -> str:
    return name[:-3] + ".html"


# ---------------------------------------------------------------------------
# Heading slugs
# ---------------------------------------------------------------------------

def heading_slug(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return s or "section"


# ---------------------------------------------------------------------------
# Block markdown -> HTML
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_LIST_ITEM_RE = re.compile(r"^(\s*)([-*+])\s+(.*)$")
_ORDERED_ITEM_RE = re.compile(r"^(\s*)(\d+[.)])\s+(.*)$")
_TABLE_ROW_RE = re.compile(r"^\s*\|(.+)\|\s*$")
_HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,})\s*$")
_CHECKBOX_RE = re.compile(r"^(\s*[-*+]\s+)\[([ xX])\]\s+(.*)$")


def is_block_start(text: str) -> bool:
    """True if a line begins a structural block (heading, list, table...)."""
    return bool(
        _HEADING_RE.match(text)
        or _LIST_ITEM_RE.match(text)
        or _ORDERED_ITEM_RE.match(text)
        or _TABLE_ROW_RE.match(text)
        or _HR_RE.match(text)
        or text.lstrip().startswith(">")
        or text.startswith("```")
    )


def md_to_html(md_text: str) -> str:
    lines = md_text.split("\n")
    i = 0
    n = len(lines)
    out: List[str] = []

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        heading_match = _HEADING_RE.match(line)
        if heading_match:
            level = min(len(heading_match.group(1)), 6)
            content = _inline(heading_match.group(2).strip())
            out.append(
                f'<h{level} id="{heading_slug(heading_match.group(2))}">{content}</h{level}>'
            )
            i += 1
            continue

        if _HR_RE.match(line) and not _TABLE_ROW_RE.match(line):
            out.append("<hr>")
            i += 1
            continue

        if line.startswith("```"):
            i += 1
            code_lines: List[str] = []
            while i < n and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
            continue

        if line.lstrip().startswith(">"):
            quote_lines: List[str] = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + md_to_html("\n".join(quote_lines)) + "</blockquote>")
            continue

        if _TABLE_ROW_RE.match(line):
            rows: List[str] = []
            while i < n and _TABLE_ROW_RE.match(lines[i]):
                rows.append(_TABLE_ROW_RE.match(lines[i]).group(1))
                i += 1
            header_cells: Optional[List[str]] = None
            if len(rows) >= 2 and re.fullmatch(r"[\s:|-]+", rows[1]):
                header_cells = [c.strip() for c in rows[0].split("|")]
                rows = rows[2:]
            out.append("<table>")
            if header_cells:
                out.append("<thead><tr>")
                for cell in header_cells:
                    out.append(f"<th>{_inline(cell)}</th>")
                out.append("</tr></thead>")
            out.append("<tbody>")
            for row in rows:
                cells = [c.strip() for c in row.split("|")]
                out.append("<tr>")
                for cell in cells:
                    out.append(f"<td>{_inline(cell)}</td>")
                out.append("</tr>")
            out.append("</tbody></table>")
            continue

        if _LIST_ITEM_RE.match(line) or _ORDERED_ITEM_RE.match(line):
            i = _convert_list(lines, i, out)
            continue

        # paragraph
        para: List[str] = [line]
        i += 1
        while i < n:
            nxt = lines[i]
            if not nxt.strip() or is_block_start(nxt):
                break
            para.append(nxt)
            i += 1
        out.append("<p>" + _inline(" ".join(p.strip() for p in para)) + "</p>")

    return "\n".join(out)


def _convert_list(lines: List[str], i: int, out: List[str]) -> int:
    """Convert a bullet/numbered list, handling one level of nesting."""
    first_match = _LIST_ITEM_RE.match(lines[i]) or _ORDERED_ITEM_RE.match(lines[i])
    ordered = bool(re.match(r"\d+[.)]$", first_match.group(2)))
    base_indent = len(first_match.group(1))
    tag = "ol" if ordered else "ul"
    n = len(lines)
    out.append(f"<{tag}>")
    pending: Optional[str] = None

    def flush() -> None:
        nonlocal pending
        if pending is not None:
            out.append(f"<li>{pending}</li>")
            pending = None

    while i < n:
        line = lines[i]
        m = _LIST_ITEM_RE.match(line) or _ORDERED_ITEM_RE.match(line)
        if m is None or len(m.group(1)) < base_indent:
            break
        if len(m.group(1)) > base_indent:
            # nested list (or contained in nothing; emit as a sibling block)
            flush()
            i = _convert_list(lines, i, out)
            continue
        checkbox = _CHECKBOX_RE.match(line)
        raw_item = (checkbox or m).group(3)
        # continuation lines (indented prose continuing a list item);
        # accumulate raw text first so markers spanning wrapped lines stay paired
        while (
            i + 1 < n
            and lines[i + 1].strip()
            and lines[i + 1][0] in " \t"
            and _LIST_ITEM_RE.match(lines[i + 1]) is None
            and _ORDERED_ITEM_RE.match(lines[i + 1]) is None
            and not is_block_start(lines[i + 1])
        ):
            i += 1
            raw_item += " " + lines[i].strip()
        if checkbox:
            state = "checked" if checkbox.group(2).lower() == "x" else ""
            item_text = (
                f'<input type="checkbox" disabled {state}> ' + _inline(raw_item)
            )
        else:
            item_text = _inline(raw_item)
        if pending is not None:
            out.append(f"<li>{pending}</li>")
        pending = item_text
        i += 1
    flush()
    out.append(f"</{tag}>")
    return i


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — The Audiobook Recording Handbook</title>
<meta name="description" content="A warm, plain-English handbook for recording your own audiobook at home: bedroom acoustics, free Audacity setup, store specs in plain numbers, reading tips for non-voice-actors, a chapter-by-chapter workflow, and honest narration options.">
<style>
:root {{
  --ink: #23201a;
  --paper: #fdfbf7;
  --accent: #7c3f2d;
  --accent-soft: #f3e6df;
  --line: #e4dcd2;
  --muted: #6f675c;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
  line-height: 1.65;
  font-size: 18px;
}}
.wrap {{ max-width: 46em; margin: 0 auto; padding: 1.2rem 1.2rem 4rem; }}
header.site {{
  border-bottom: 3px double var(--line);
  padding: 1.3rem 0 1rem;
  margin-bottom: 1rem;
}}
header.site h1 {{ margin: 0 0 .2rem; font-size: 1.45rem; }}
header.site h1 a {{ color: var(--accent); text-decoration: none; }}
header.site p.tag {{ margin: 0; color: var(--muted); font-style: italic; }}
nav.toc {{
  background: var(--accent-soft);
  border-radius: 8px;
  padding: .9rem 1.1rem;
  margin: 1.3rem 0 1.8rem;
  font-size: .95rem;
}}
nav.toc ol {{ margin: .2rem 0 .2rem 1.2rem; padding: 0; }}
nav.toc li {{ margin: .15rem 0; }}
nav.toc a {{ color: var(--ink); text-decoration: none; }}
nav.toc a:hover {{ text-decoration: underline; }}
nav.pagers {{
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  margin: 2.4rem 0 0;
  border-top: 1px solid var(--line);
  padding-top: 1rem;
  font-size: .95rem;
}}
nav.pagers a {{ color: var(--accent); text-decoration: none; font-weight: bold; }}
nav.pagers a:hover {{ text-decoration: underline; }}
h2 {{ border-bottom: 1px solid var(--line); padding-bottom: .25rem; }}
h3 {{ color: var(--accent); }}
table {{ border-collapse: collapse; width: 100%; margin: 1.1rem 0; font-size: .92em; }}
th, td {{ border: 1px solid var(--line); padding: .5rem .6rem; text-align: left; vertical-align: top; }}
th {{ background: var(--accent-soft); }}
code {{
  background: var(--accent-soft);
  padding: .05em .35em;
  border-radius: 4px;
  font-size: .9em;
  font-family: 'SFMono-Regular', Consolas, Menlo, monospace;
}}
pre {{
  background: #2d2a24;
  color: #f6f1e7;
  padding: .9rem 1.1rem;
  border-radius: 8px;
  overflow-x: auto;
  line-height: 1.45;
  font-size: .9em;
}}
pre code {{ background: none; color: inherit; padding: 0; }}
blockquote {{
  margin: 1.2rem 0;
  padding: .2rem 1.1rem;
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  border-radius: 0 8px 8px 0;
}}
ul, ol, p {{ margin: .8rem 0; }}
li {{ margin: .3rem 0; }}
footer.site {{
  margin-top: 3rem;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: .85rem;
}}
.meta {{ color: var(--muted); font-size: .85rem; margin: -.3rem 0 1.4rem; }}
input[type="checkbox"] {{ accent-color: var(--accent); }}
@media (max-width: 700px) {{ body {{ font-size: 16.5px; }} }}
</style>
</head>
<body>
<div class="wrap">
<header class="site">
<h1><a href="index.html">The Audiobook Recording Handbook</a></h1>
<p class="tag">Record your own audiobook at home — blankets beat gear</p>
</header>
{content}
<footer class="site">
<p>{meta}</p>
<p>Copyright (c) 2026 Asdale Dynamics, LLC · <a href="https://dylanasdale.github.io" target="_blank" rel="noopener">dylanasdale.github.io</a> · MIT licensed. Written plain, warm, and checked like you would if a friend asked you to test it.</p>
</footer>
</div>
</body>
</html>
"""


def _count_words(md_text: str) -> int:
    text = re.sub(r"^#{1,6}\s+.*$", "", md_text, flags=re.MULTILINE)
    text = re.sub(r"[|`>*_\-\[\]()#]", " ", text)
    return len([w for w in text.split() if w])


def md_title(md_text: str) -> str:
    for line in md_text.split("\n"):
        m = _HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:
            return m.group(2).strip()
    return "Untitled"


def discover_docs() -> List[Path]:
    files = sorted(DOCS.glob("*.md"))
    if not files:
        raise SystemExit(f"No markdown files found in {DOCS}")
    return files


def _toc_nav(current: Optional[str] = None) -> str:
    items = []
    for path in discover_docs():
        title = md_title(path.read_text(encoding="utf-8"))
        fname = path.stem + ".html"
        label = _escape(title)
        if current == fname:
            items.append(f'<li><strong>{label}</strong></li>')
        else:
            items.append(f'<li><a href="{fname}">{label}</a></li>')
    return f"<p><strong>In this handbook</strong></p><ol>{''.join(items)}</ol>"


def _pagers(path: Path) -> str:
    files = discover_docs()
    idx = files.index(path)
    parts = []
    if idx > 0:
        prev = files[idx - 1]
        prev_title = md_title(prev.read_text(encoding="utf-8"))
        parts.append(f'<a href="{prev.stem}.html">&larr; {_escape(prev_title)}</a>')
    else:
        parts.append("<span></span>")
    if idx < len(files) - 1:
        nxt = files[idx + 1]
        nxt_title = md_title(nxt.read_text(encoding="utf-8"))
        parts.append(f'<a href="{nxt.stem}.html">{_escape(nxt_title)} &rarr;</a>')
    else:
        parts.append("<span></span>")
    return f"<nav class='pagers'>{''.join(parts)}</nav>"


def make_page(title: str, content: str, meta: str) -> str:
    return PAGE_TEMPLATE.format(
        title=_escape(title),
        content=content,
        meta=meta,
    )


def build(out: Optional[Path] = None, check_only: bool = False) -> List[str]:
    """Build the site; return list of broken internal links (empty = clean)."""
    if not DOCS.exists() or not discover_docs():
        raise SystemExit(f"No markdown files found in {DOCS}")
    files = discover_docs()

    pages: List[Tuple[str, str, str]] = []
    for path in files:
        md_text = path.read_text(encoding="utf-8")
        title = md_title(md_text)
        words = _count_words(md_text)
        meta = f"{path.name.replace('_', ' ')} · {words:,} words · about {max(1, words // 200)} min to read"
        content = (
            f"<p class='meta'>{meta}</p><nav class='toc'>{_toc_nav(path.stem + '.html')}</nav>"
            + md_to_html(md_text)
            + _pagers(path)
        )
        pages.append((path.stem + ".html", title, make_page(title, content, meta)))
    index_html = make_index_page()
    pages.append(("index.html", "The Audiobook Recording Handbook", index_html))

    valid_targets = {p[0] for p in pages}

    broken: List[str] = []
    for fname, _title, page_html in pages:
        for href in re.findall(r'href="([^"]+)"', page_html):
            head = href.split("#")[0]
            if not head or head.startswith(("http://", "https://", "mailto:")):
                continue
            if head not in valid_targets:
                broken.append(f"{fname} -> {href}")

    if not check_only and out is not None:
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        for fname, _t, page in pages:
            (out / fname).write_text(page, encoding="utf-8")
    return broken


def make_index_page() -> str:
    files = discover_docs()
    items = []
    for path in files:
        md_text = path.read_text(encoding="utf-8")
        title = md_title(md_text)
        items.append(f'<li><a href="{path.stem}.html">{_escape(title)}</a></li>')
    first = files[0]
    first_text = first.read_text(encoding="utf-8")
    first_body = first_text.split("\n", 1)[1] if "\n" in first_text else ""
    content = (
        "<nav class='toc'><p><strong>What's inside</strong></p><ol>"
        + "".join(items)
        + "</ol></nav>"
        + md_to_html(first_body)
    )
    words = _count_words(first_text)
    meta = f"Built {datetime.date.today().isoformat()}"
    return make_page("Home", content, meta)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="output directory (default: site/)")
    ap.add_argument("--check", action="store_true", help="validate docs and links without writing")
    args = ap.parse_args()

    try:
        broken = build(out=Path(args.out), check_only=args.check)
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        print(f"build failed: {exc}", file=sys.stderr)
        return 1

    if broken:
        print("BROKEN INTERNAL LINKS:")
        for b in broken:
            print("  " + b)
        return 2
    if args.check:
        print(f"check OK: {len(discover_docs())} docs, all internal links resolve")
        return 0
    print(f"Built {len(discover_docs()) + 1} pages -> {Path(args.out).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
