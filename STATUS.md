# STATUS.md — Audiobook Recording Handbook

Built: October 26, 2026 · Maintained by Asdale Dynamics, LLC

## What was built

A complete, author-friendly manual for recording your own audiobook at home,
published as both Markdown (`docs/`) and a self-built static HTML site.

**Content (10 chapters):**

| File | Chapter |
|---|---|
| docs/00-intro.md | Introduction: who this is for, how to use it |
| docs/01-bedroom-basics.md | Bedroom recording basics — blankets beat gear; noise audit |
| docs/02-free-audacity-setup.md | Free Audacity setup in five minutes |
| docs/03-acx-specs.md | Store specs (ACX-style) in plain numbers, with exact Audacity recipes |
| docs/04-reading-tips.md | Reading tips for non-voice-actors |
| docs/05-chapter-workflow.md | Chapter-by-chapter workflow: prep → record → edit → master → export |
| docs/06-narration-options.md | DIY vs narrator hiring vs free AI narration, with honest limits |
| docs/07-listening-and-publishing.md | Final listen, stores, pricing, launch |
| docs/08-checklists.md | Print-and-tape checklists (setup / session / take / delivery / pickups) |
| docs/09-glossary.md | Plain-English glossary of every term used |

**Tooling:**

- `build.py` — dependency-free static site builder (Python 3.9+, stdlib only).
  Converts every chapter, adds a warm styled template with a per-page table
  of contents, prev/next pagers, cross-page internal links (`.md` → `.html`),
  auto-generated `index.html`, and a footer credit + copyright line.
  Validates all internal links and fails with a nonzero exit code if any are
  broken. Modes: `build`, `--check` (validate only), `--out DIR`.
- `test_build.py` — 34 tests via Python's built-in unittest: unit tests for
  the markdown converter (headings, paragraphs, lists, tables, blockquotes,
  code blocks, checkboxes, inline markup incl. nested italics-in-bold and
  links), content guard tests (H1s present, no unbalanced markers, no stray
  non-Latin characters, no secrets/email patterns), and integration tests
  that run the real build into a temp directory and verify pages, nav,
  links, and leak-free rendering. CLI invocation is tested too.
- No third-party dependencies, no network access, no secrets, API keys, or
  personal data anywhere in the repo.

## How to run it

```bash
python3 build.py            # build the static site into site/
python3 build.py --check    # validate docs + links, write nothing
python3 -m unittest test_build -v   # run the test suite
```

Then open `site/index.html` in any browser. Nothing is published anywhere;
the site is plain local files.

## Verification results

- `python3 build.py` → `Built 11 pages -> .../site` (10 chapters + index). ✅
- `python3 build.py --check` → `check OK: 10 docs, all internal links resolve`. ✅
- `python3 -m unittest test_build` → `Ran 34 tests ... OK`. ✅
- Automated leak sweeps over generated HTML for raw `**` markers, escaped
  `<strong>` tags, raw table separators, and stray non-Latin characters: clean. ✅
- Manual read-through of all rendered pages: formatting, tables, checklists
  (checkbox inputs), and code blocks render correctly. ✅

## Known gaps / honest limits

- Store specs, distribution programs, and AI-narration options change
  frequently. Chapters 3 and 6 teach the shape of the landscape and use
  conservative, careful language, and every chapter tells the reader to
  re-check the current published spec sheets at the source before upload.
  No live numbers beyond the long-stable ACX-style core (44.1 kHz, mono,
  192 kbps constant, -3 dB peak, `-23…-18 dB` RMS, -60 dB noise floor,
  room tone, 120-minute file cap).
- The site is generated fresh on each build; `site/` output is committed so
  the folder works offline immediately after checkout.
- The markdown converter covers the subset this handbook actually uses
  (headings h1–h4, paragraphs, ordered/bullet lists incl. checkboxes, tables,
  blockquotes, fenced code, inline code/bold/italic/links). It is not a
  general-purpose Markdown parser; a rendered-title test and leak guards are
  in place so unrecognized constructs surface loudly in tests.
- Cross-references to the sibling guide *Publishing Beyond KDP* are by name
  (it lives in its own repository); links to store websites in the docs are
  avoided in favor of naming sources to check.
