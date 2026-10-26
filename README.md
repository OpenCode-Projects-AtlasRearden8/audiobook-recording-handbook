# The Audiobook Recording Handbook

A warm, plain-English handbook for **recording your own audiobook at home** —
bedroom acoustics where blankets beat gear, a free Audacity setup,
audiobook-store specs translated into plain numbers, reading tips for
non-voice-actors, a chapter-by-chapter workflow, and an honest guide to your
three narration routes (record it yourself / hire a narrator / free AI
narration).

Written the way we like explaining things: like a friend would. Never
condescending, always concrete.

## What's inside

```
docs/            # the handbook itself — 10 markdown chapters
├── 00-intro.md                       who this is for, how to use it
├── 01-bedroom-basics.md              blanket booths and noise audits
├── 02-free-audacity-setup.md         the free five-minute setup
├── 03-acx-specs.md                   store specs in plain numbers
├── 04-reading-tips.md                for non-voice-actors
├── 05-chapter-workflow.md            prep → record → edit → master → export
├── 06-narration-options.md           DIY vs hire vs free AI, honestly
├── 07-listening-and-publishing.md    stores, pricing, launch
├── 08-checklists.md                  print-and-tape checklists
└── 09-glossary.md                    every term in plain English
build.py         # dependency-free static site builder (Python stdlib only)
test_build.py    # tests for the converter and the build (unittest)
site/            # the generated static site (committed output)
```

## How to build

Local-first and dependency-free: only Python 3.9+ is required. Nothing is
downloaded, nothing is uploaded.

```bash
python3 build.py            # build site/ from docs/
python3 build.py --check    # validate docs and internal links, write nothing
python3 build.py --out DIR  # build into a different directory
```

Open `site/index.html` in any browser to read the built handbook.

## How to test

```bash
python3 -m unittest test_build -v
```

The tests cover the markdown-to-HTML converter (unit tests), guard the actual
handbook content against formatting leaks and stray characters, and run the
real build into a temporary directory (integration tests), verifying that
every page renders, every internal link resolves, and no secrets or markers
leak into the HTML.

## Using the handbook

Read the chapters in order the first time. After that, `08-checklists.md` is
designed to be printed and taped to your recording desk, and `09-glossary.md`
is the plain-English translation table for anything that felt like jargon.

## Complementary guides

This handbook pairs with our **Publishing Beyond KDP** guide, which covers
wide distribution, and with everything at
[dylanasdale.github.io](https://dylanasdale.github.io).

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
