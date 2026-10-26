# ACX-Style Specs in Plain Numbers

When you upload an audiobook to Amazon, Audible, or ACX (Amazon's audiobook
program), their checker measures your audio against a spec sheet. This
chapter translates every line of that spec sheet into plain numbers and
plain English.

**Why copy the strictest spec?** Because Amazon/Audible is the strictest of
the big stores. If your files pass here, they pass nearly everywhere else.
(Apple, Spotify, Findaway, and the rest are the same or slightly looser.)

## The full spec, translated

| Spec line | Plain number | What to do |
|---|---|---|
| Format | MP3, 192 kbps **or higher**, constant bit rate, mono | Export mono, then convert; this is the last step |
| Sample rate | **44100 Hz** (44.1 kHz) | Set in Audacity project rate; keep it everywhere |
| Peak level | **-3 dB or lower**, never higher | Peak normalization after mastering |
| RMS loudness | **-23 dB to -18 dB** (Audible standard) | The mastering "Loudness" step |
| Noise floor | **-60 dB RMS or lower** | Fixed by your room (Chapter 1), mostly |
| Room tone | **1–5 seconds** at the start of every file (and ~1 second at the end) | Copy-paste from your noise profile |
| Max file length | **120 minutes** or less per file | A "chapter" file (rarely). Split if needed |
| Credits | Opening: book title + chapter; Closing: read narration ending | Optional at some stores, required at ACX |
| Chapters as files | One file per chapter (or roughly) | Chapter 5 outlines filenames |

> **Important:** Stores tweak specs occasionally, and distribution programs
> keep evolving (for example, Audible tightened how open ACX is to third
> parties in recent years, and Spotify's audiobook programs are still
> changing shape as of writing). Always check the current published spec
> sheet at whichever store you plan to upload to before your final export.
> This handbook teaches you the *shape* of the spec and one complete,
> sensible recipe; confirm today's exact numbers at the source.

## What each number actually means

### Peak level: -3 dB

Every audio file has a loudest instant — the **peak**. Peaks hitting 0 dB
("full scale") start clipping, which sounds like crackle and cannot be
un-clipped after export. The spec asks you to leave 3 dB of headroom:
imagine a cliff edge; peaks should stop 3 decibels short of the edge.

In practice: if your loudest shouted moments *just barely* reach -3 dB, and
your quietest spoken words are around -20 to -30 dB, you're set.

### RMS loudness: -23 to -18 dB

Where peak is the *draw of the highest wave* — one instant — **RMS** is
roughly "average loudness of the spoken words". Think of it as the level of
your *steady talking voice*, not your loudest yell.

- -18 dB RMS: the loud end (energetic, close-mic'd audio)
- -23 dB RMS: the quiet end (the minimum most stores accept)

If your narration sounds good at conversational volume through headphones,
you're probably in the zone. Audacity measures RMS for you (see below) so
you don't have to guess.

### Noise floor: -60 dB or lower

The **noise floor** is the constant background level — your room's hum,
your mic's self-noise, your pairing of computer-fan and breath. At -60 dB
it's essentially inaudible under narration, and it's the level pro studios
actually achieve with expensive gear.

If Chapter 1's blanket booth is in place and the noise audit is done, you
should hit -60 dB RMS floor with any decent USB dynamic mic. If you're at
-40 or -50, fix the room first — no plugin does this magically.

### Room tone: 1–5 seconds

Stores want a little silence at the start of every file so their playback
and transition systems sound smooth between chapters. **Room tone** means
"the sound of your room with nobody in it". In practice:

- Record ~5 seconds of silence at the start of each session (do this
  *before* your first read, and keep it).
- In editing, trim each chapter file so it starts with about **3 seconds**
  of that room tone and ends with about **1 second** of it.
- Copy-paste this room tone from one file into the beginning of a chapter
  file if you lose it.

### The 44100 Hz number

Audio files store "snapshots" of sound per second — the sample rate. 44100
Hz captures everything a human ear hears on speech and music, and it's the
CD standard that every audiobook store asks you for. Set it once in
Audacity's bottom right corner (project rate) and never think about it
again. Exporting at a different rate is the #1 spec-fail we see, and it's
totally avoidable with one dropdown.

## How to actually hit these numbers in Audacity (free, no plugins)

For each chapter after editing (Chapter 5 runs these in order):

Two steps cover the level requirements, in this order:

1. **Loudness normalization (set the RMS window first):**
   Select all (Ctrl+A) → Effect → **Loudness Normalization**.
   - Select **Perceived loudness (LUFS)** as the mode, and set the target to
     **-19 LUFS** for mono audiobook delivery. (Single-channel (mono) audio
     understood this way lands in the required -23 to -18 dB RMS window; -19
     LUFS reads out roughly around **-21 dB RMS**, comfortably inside.)
   - Leave the other controls as defaults and click OK.

2. **Peaks to -3 dB (only if needed):**
   Select all again → Effect → **Amplify**. Audacity pre-fills the
   "New Peak Amplitude" box with the ceiling value; **type -3.0 into the New
   Peak Amplitude box** and click OK. Now the loudest instant of the file
   sits at -3 dB.
   - If Amplify is grayed out, your peak is already at or below -3 dB —
     skip it.
   - The modest whole-file shift here pushes your RMS down by the same
     number of decibels, which almost never knocks a -19 LUFS mono file out
     of the 5 dB-wide RMS window. If you're one of the rare cases, re-run
     step 1 and leave a little more mic distance next session.

Everything else (trim the head/tail, wash the noise floor, export):

3. **Trim, room tone, check:**
   Head: ~3 seconds of room tone. Tail: ~1 second. No chopped-off breath.

4. **Measure, don't hope** (optional but recommended):
   Select a silent 2-second stretch of room tone and open **Analyze → Plot
   Spectrum**. For a -60 dB-class noise floor, the lowest curve hugs the
   bottom of the chart around **-60 dB or below** through the mid
   frequencies. If you see a floor at -35 or -45 dB, room noise is audible
   under narration — go back to Chapter 1 and add blankets.

5. **Export WAV first, MP3 last:**
   - Working file: **File → Export → Export as WAV**, 44100 Hz, 32-bit
     float, mono.
   - Delivery file: **File → Export → Export as MP3**, Bit Rate Mode =
     **Constant**, Quality = **192 kbps** (or higher), Channel Mode =
     **Forced stereo?** No — Force mono if the option exists; if you
     recorded in mono the export will be mono anyway. Set 44100 Hz sample
     rate. Add ID3v2 metadata if asked (see Chapter 5 for naming).

> **Quick sanity check:** play your exported MP3 in any player at moderate
> volume on headphones and on speakers. It should sound like a clean,
> comfortable, evenly-loud voice with silence at both ends. That _feel_,
> plus the numbers above, is the whole spec.

## A note about "mastering"

The word sounds intimidating; in a home audiobook context it means exactly
the three steps above: **edit, then set peaks to -3 dB, then set RMS into
spec range, then export.** No magic, no mystique. Chapter 5 slots these
steps into your per-chapter workflow so it becomes muscle memory by
chapter three.
