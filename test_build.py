#!/usr/bin/env python3
"""Tests for the audiobook-recording-handbook build.

Run:  python3 test_build.py   (or: python3 -m unittest test_build -v)

Covers:
- unit tests for the markdown converter (headings, paragraphs, lists,
  tables, blockquotes, code blocks, inline markup, checkboxes, links)
- an integration test that actually runs build.build() into a temp dir
and verifies pages, nav, links, and leak-free rendering.
"""

from __future__ import annotations

import re
import shutil
import tempfile
import unittest
from pathlib import Path

import build as build_mod


ROOT = Path(__file__).resolve().parent


class InlineTests(unittest.TestCase):
    def test_plain_text_is_escaped(self):
        self.assertEqual(build_mod._inline("A & B"), "A &amp; B")
        self.assertEqual(build_mod._inline("<script>"), "&lt;script&gt;")

    def test_bold(self):
        self.assertEqual(build_mod._inline("**hot**"), "<strong>hot</strong>")

    def test_italic(self):
        self.assertEqual(build_mod._inline("*calm*"), "<em>calm</em>")

    def test_bold_then_italic(self):
        # sequence of independent markers
        got = build_mod._inline("**one** and *two*")
        self.assertEqual(got, "<strong>one</strong> and <em>two</em>")

    def test_italic_inside_bold(self):
        got = build_mod._inline("**Breathe *before* thinking**")
        self.assertEqual(
            got, "<strong>Breathe <em>before</em> thinking</strong>"
        )

    def test_bold_multiple_pairs(self):
        got = build_mod._inline("**A** and **B**")
        self.assertEqual(got, "<strong>A</strong> and <strong>B</strong>")

    def test_code_span(self):
        got = build_mod._inline("`projects/ch01.aup3`")
        self.assertEqual(got, "<code>projects/ch01.aup3</code>")

    def test_code_angles_escaped(self):
        got = build_mod._inline("`a < b`")
        self.assertEqual(got, "<code>a &lt; b</code>")

    def test_external_link(self):
        got = build_mod._inline("[Audacity](https://audacityteam.org)")
        self.assertIn('href="https://audacityteam.org"', got)
        self.assertIn("target=\"_blank\"", got)
        self.assertIn(">Audacity</a>", got)

    def test_internal_md_link_converts(self):
        got = build_mod._inline("[Glossary](09-glossary.md)")
        self.assertEqual(got, '<a href="09-glossary.html">Glossary</a>')

    def test_internal_anchor_link(self):
        got = build_mod._inline("[Peaks](03-acx-specs.md#peak-level)")
        self.assertEqual(got, '<a href="03-acx-specs.html#peak-level">Peaks</a>')

    def test_unbalanced_bold_left_alone(self):
        got = build_mod._inline("two ** stars")
        self.assertEqual(got, "two ** stars")


class BlockTests(unittest.TestCase):
    def test_heading(self):
        out = build_mod.md_to_html("# Hello World")
        self.assertEqual(out, '<h1 id="hello-world">Hello World</h1>')

    def test_paragraphs_join_soft_lines(self):
        out = build_mod.md_to_html("one line\nwrapped\n\nsecond")
        self.assertIn("<p>one line wrapped</p>", out)
        self.assertIn("<p>second</p>", out)

    def test_bullet_list(self):
        out = build_mod.md_to_html("- apples\n- pears\n").replace("\n", "")
        self.assertEqual(out, "<ul><li>apples</li><li>pears</li></ul>")

    def test_ordered_list(self):
        out = build_mod.md_to_html("1. first\n2. second\n").replace("\n", "")
        self.assertEqual(out, "<ol><li>first</li><li>second</li></ol>")

    def test_nested_list_becomes_sibling(self):
        out = build_mod.md_to_html("- parent\n  - child\n").replace("\n", "")
        self.assertEqual(out, "<ul><li>parent</li><ul><li>child</li></ul></ul>")

    def test_checkbox_item(self):
        out = build_mod.md_to_html("- [ ] water\n- [x] mic\n")
        self.assertIn('<input type="checkbox" disabled > water', out)
        self.assertIn('<input type="checkbox" disabled checked> mic', out)

    def test_table(self):
        out = build_mod.md_to_html("| A | B |\n|---|---|\n| 1 | 2 |\n").replace("\n", "")
        self.assertIn("<thead><tr><th>A</th><th>B</th></tr></thead>", out)
        self.assertIn("<tr><td>1</td><td>2</td></tr>", out)

    def test_table_cells_get_inline_markup(self):
        out = build_mod.md_to_html("| A | B |\n|---|---|\n| **hot** | x |\n").replace("\n", "")
        self.assertIn("<td><strong>hot</strong></td>", out)

    def test_blockquote(self):
        out = build_mod.md_to_html("> sage advice\n> more lines")
        self.assertIn("<blockquote>", out)
        self.assertIn("sage advice", out)

    def test_fenced_code_block(self):
        out = build_mod.md_to_html("```\nsome <code>\n```\n")
        self.assertIn("<pre><code>some &lt;code&gt;</code></pre>", out)

    def test_hr(self):
        out = build_mod.md_to_html("before\n\n---\n\nafter")
        self.assertIn("<hr>", out)

    def test_heading_slug(self):
        self.assertEqual(build_mod.heading_slug("The ACX — Specs (2026)"), "the-acx-specs-2026")
        self.assertEqual(build_mod.heading_slug("Hello, World!"), "hello-world")


class DocContentTests(unittest.TestCase):
    """Guard tests for the actual handbook files."""

    def setUp(self):
        self.files = build_mod.discover_docs()
        self.assertTrue(self.files, "no docs found")

    def test_docs_have_h1_titles(self):
        for path in self.files:
            title = build_mod.md_title(path.read_text(encoding="utf-8"))
            self.assertNotEqual(title, "Untitled", f"{path.name} has no H1")

    def test_no_markdown_leaks_when_rendered(self):
        for path in self.files:
            rendered = build_mod.md_to_html(path.read_text(encoding="utf-8"))
            self.assertFalse(
                re.search(r"\*\*[^<]{0,80}\*\*", rendered),
                f"{path.name} left raw ** markers in the HTML",
            )
            self.assertFalse(
                re.search(r"(?<!&)lt;strong&gt;", rendered),
                f"{path.name} has escaped <strong> tags in the HTML",
            )
            self.assertFalse(
                re.search(r"\|---\|", rendered),
                f"{path.name} left a raw table separator in the HTML",
            )

    def test_no_injected_errors_like_stray_markers(self):
        for path in self.files:
            text = path.read_text(encoding="utf-8")
            # catch corrupted artifacts from bad generations (garbled
            # placeholder words, CJK stray characters, mangled code)
            stray = re.findall(r"[\u4e00-\u9fff\u0400-\u04ff]", text)
            self.assertFalse(stray, f"{path.name} contains non-Latin stray chars: {stray[:3]}")

    def test_no_secrets_or_personal_data(self):
        patterns = [
            re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]"),
            re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),  # email addresses
        ]
        for path in self.files:
            text = path.read_text(encoding="utf-8")
            for p in patterns:
                self.assertIsNone(
                    p.search(text),
                    f"{path.name} contains a possible secret/personal-data pattern: {p.pattern}",
                )


class BuildIntegrationTests(unittest.TestCase):
    """Run the real build into a temp directory."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="handbook-test-"))
        self.out = self.tmp / "site"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_produces_pages_and_clean_links(self):
        broken = build_mod.build(out=self.out)
        self.assertEqual(broken, [], f"broken links: {broken}")
        docs = build_mod.discover_docs()
        page_files = sorted(p.name for p in self.out.glob("*.html"))
        expected = sorted(p.stem + ".html" for p in docs) + ["index.html"]
        self.assertEqual(page_files, expected)
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            self.assertIn("The Audiobook Recording Handbook", text)
            self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)
            self.assertFalse(re.search(r"\*\*[^<]*\*\*", text), f"markdown leak in {page.name}")

    def test_check_mode_does_not_write(self):
        broken = build_mod.build(out=self.out, check_only=True)
        self.assertEqual(broken, [])
        self.assertFalse(self.out.exists())  # nothing written in check mode

    def test_index_links_all_pages(self):
        build_mod.build(out=self.out)
        index = (self.out / "index.html").read_text(encoding="utf-8")
        for doc in build_mod.discover_docs():
            self.assertIn(f'href="{doc.stem}.html"', index)

    def test_nav_on_each_page(self):
        build_mod.build(out=self.out)
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            if page.name == "index.html":
                continue
            self.assertIn("In this handbook", text, f"{page.name} missing TOC nav")


class CliTests(unittest.TestCase):
    def test_cli_check_returns_zero(self):
        import subprocess
        proc = subprocess.run(
            ["python3", str(ROOT / "build.py"), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0,proc.stdout + proc.stderr)

    def test_cli_build_returns_zero(self):
        import subprocess
        with tempfile.TemporaryDirectory(prefix="hb-cli-") as tmp:
            proc = subprocess.run(
                ["python3", str(ROOT / "build.py"), "--out", str(Path(tmp) / "s")],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
