# The Chapter-by-Chapter Workflow

This chapter is your day-to-day playbook. Once your room is set (Chapter 1)
and Audacity is configured (Chapter 2), recording a whole book is just this
loop, repeated once per chapter:

**prep → record → self-edit → check against specs → master → export →
log and rest**

One chapter at a time, every time. The single biggest cause of abandoned
audiobooks is trying to "record the whole book first, edit later". Don't.
Per-chapter is faster, better, kinder to your voice, and recoverable.

## The folder layout that never fails

Set this up once, before chapter 1:

```
my-audiobook/
├── manuscript/          # one PDF/text per chapter, recorder copy
│   ├── ch01.pdf
│   └── ...
├── projects/            # Audacity working projects (never uploaded)
│   ├── ch01.aup3
│   └── ...
├── masters/             # checked WAV masters (kept as backup)
│   └── ch01-master.wav
├── deliver/             # final MP3s ready to upload
│   └── 01_The_Beginning.mp3
├── pickup-notes/        # little text files of retakes to grab
│   └── ch01-notes.txt
└── LOG.md               # one line per session (see below)
```

Naming for delivery files: **zero-padded, plain, sortable**, e.g.
`03_Cold_Evidence.mp3`. No spaces in extensions, no emoji, no version soup.
Opening and closing title files (if your store wants them) become
`00_Opening.mp3` and `99_Closing.mp3`.

## Chapter 1 of a chapter: prep (10 minutes)

1. **Save the manuscript copy** for this chapter into `manuscript/`
   (recorder's copy: bigger font, wide margins, penciled notes allowed).
2. **Pre-read it once** silently-aloud, marking emphasis, pauses, unknown
   pronunciations (Chapter 4 technique).
3. **Check the room**: 30 seconds of silent listening at full volume
   (headphones) before you start. If anything hums, fix it now, not after
   two chapters of confusion.
4. **Water, apple, notes, log line open.** Start the session log line:
   `2026-03-14 19:00 ch07 — session 1`.

## Record (45–90 minutes)

1. Open the chapter's **new** Audacity project (`projects/ch07.aup3`,
   44100 Hz project rate).
2. **Record ~5 seconds of room tone first**: "session tone", silence,
   nothing. Leave it at the top of the project. (Chapter 3's spec needs
   this.)
3. Read. On a flub: 1-second pause, back to the start of the phrase, re-read,
   continue. No "sorry". (Chapter 4 explains.)
4. Between sections (scene break, chapter break, after any long pause for a
   stretch): record a **fresh 2–3 seconds of room tone** as a spacer. This
   doesn't cost anything and gives the editor clean splices.
5. **Ctrl+S after every take.** Not "at the end of the session" — after
   every take.

Session rhythm that works well for most authors:

- Read for 25–30 minutes. Stop, drink water, stand up.
- **Skim-listen to 30 seconds of each new section immediately** while it's
  fresh. You aren't editing yet — just verifying the section is flub-clean
  and not too quiet on your mic.
- Continue. 90 minutes total is a full session for most voices (Chapter 4:
  the fatigue rule).

## Self-edit (30–60 minutes per finished hour)

In the same project, an hour of raw audio usually edits down in *less* time
than it took to record once you get the hang of it:

1. **Find the mistakes visually first.** Play at normal speed over each
   section you flagged as you recorded them. Flubs live between your
   re-read pauses — Audacity's waveform (zoomed in) shows the one-second
   silences clearly.
2. **Cutting a flub:** select the flub up to the *end of the cleanly
   re-read phrase*; cut (Ctrl+X); done. Leave big natural pauses — they
   sound honest.
3. **Trim excess silence** longer than ~1.5 seconds down to that (leaving
   breath is fine; a 9-second "staring at paragraph" pause is not).
4. **Mind the breath attack the wrong way:** leave most breaths in! Only
   remove the harsh, loud, end-of-line ones, and cut *around* them without
   clipping the word that came before.
5. Room tone maintenance: where you cut, keep the sound continuous.
   Paste-session room tone (from the top of the project) under any splice
   that sounds "unsupported". Subtle, cheap, invisible.
6. Delete the session's first 5 seconds of "session tone" from the top of
   the chapter body — you'll place its own room tone in the export next.

> Later chapters get faster. By chapter 4–5, editing is your evening podcast
> time with headphones and a slightly slower podcast.

## Master, then check specs (15 minutes)

Run Chapter 3's recipe, in order, on the whole edited chapter:

1. Amplify / peak to **-3 dB max**.
2. **Loudness normalization** to ~-19 LUFS (subject to the plain-number spec
   sheet).
3. **Head/tail:** ~3 seconds room tone at the top, ~1 second at the tail.
4. Optional: check noise floor on a selected room-tone stretch (Plot
   Spectrum at around -60 dB or below).

If a check that involves "your room noise didn't get fixed" keeps failing,
no amount of mastering will save it — improving the blanket booth by one
more blanket will.

## Export (2 minutes, per chapter)

1. **File → Export → Export as WAV** → `masters/ch07-master.wav`
   (44100 Hz, 32-bit float if offered, mono).
2. **File → Export → Export as MP3** → `deliver/07_Your_Chapter_Name.mp3`
   (constant bit rate, 192 kbps, 44100 Hz, mono).
3. **Ctrl+S the project once more**, then close it.
4. Update the session log line:
   `2026-03-14 20:15 ch07 — session 1: recorded 41 min, edited, mastered, exported. DONE ✓`

That one log line is quietly why you'll finish this audiobook. Momentum you
can see beats momentum you can't.

## Pick-up sessions (20 minutes)

After exporting a chapter, you'll occasionally take a day's break, listen
to the MP3 next morning, and hear one phrase that feels *off* (too rushed,
odd emphasis, a syllable flub you missed).

- Open the project, record the replacement phrase right into the timeline
  (using the same mic distance as that session; the room tone will carry
  the continuity), edit it in, re-run the master steps, re-export.
- Same filename, overwrite. Done in 20 minutes.

This is normal, expected, and cheap. It's also the difference between
"author-recorded" and "finished".

## Momentum math (why chapter-by-chapter wins)

Per chapter of nonfiction (~5,000 words ≈ 35 minutes of finished audio):

| Step | Beginner | After 5 chapters |
|---|---|---|
| Prep + pre-read | 15 min | 12 min |
| Record | 90 min | 55 min |
| Edit | 50 min | 25 min |
| Master + export | 20 min | 12 min |
| **Total** | **~3 hours** | **~1h 45m** |

A whole novel-length book lands around **12–30 hours of work**, spread over
as many weeks as you like. A $200-per-finished-hour pro alternative for the
same book costs $1,500–$3,000. Every hour of this workflow is worth about
$100–$200 to you. It compounds with practice.
