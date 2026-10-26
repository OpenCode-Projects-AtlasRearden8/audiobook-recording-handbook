# Free Audacity Setup: Five Minutes, No Money, No Tears

Audacity is free, runs on Windows/Mac/Linux, and has been quietly recording
publishable audiobooks for over twenty years. There is no "pro tool" you need
instead of it — it's just you, Audacity, and about five minutes of setup.

## Getting Audacity

1. Go to the official site: **audacityteam.org** (the `.org` — download only
   from there).
2. Download the installer for your OS and run it.
3. First launch: click through the welcome screen; check the Audio Host
   dropdown (keep it as **MME** on Windows unless something's odd; **Core
   Audio** on Mac; **ALSA** on Linux).

> Look at the version number when you install. Audacity updates add little
> niceties now and then; any version from the last couple of years is fine
> for our purposes.

## Setting your devices (one time)

On the toolbar you'll see two dropdowns next to a microphone icon and a
speaker icon:

- **Input (microphone):** pick your recording mic. Not "default", not your
  laptop's built-in mic — the *name* of your mic.
- **Playback (speakers):** your headphones, so you can hear takes without
  loopback noise.

Then open **Edit → Preferences → Audio** (Windows/Linux) or **Audacity →
Settings → Audio** (Mac):

- **Sample rate:** leave at **44100 Hz** for everything. (Chapter 3 will
  explain why this number is golden.)
- **Recording quality:** 32-bit float if offered (it usually is) — it
  protects you from clipping quietly in the background.
- **Playback quality:** defaults are fine.

## Turning off the two settings that ruin audiobooks

Two Audacity defaults are actively harmful for this genre. Fix them once:

1. **Click "Overdub / Software playthrough" OFF** if you see it in
   Transport settings. Hearing yourself in real time while recording a long
   narration makes most people stumble. Narration is you *reading*;
   monitoring the live feed is for music overdubs, not prose.
2. **Turn "Sound Activated Recording" OFF** unless you have a specific
   reason. You want full manual control of starts and stops.

## Your window layout

You'll see four main regions. Quick tour:

- **Top toolbar:** transport buttons — record (red), play, stop, pause,
  skip to start/end. You'll live here.
- **Track view:** where your recorded audio shows up as big blue squiggles
  (waveforms). Multiple takes stack as separate tracks.
- **Left of each track:** name, volume, pan, Mute/Solo, and the Track
  dropdown menu.
- **Vertical sliders (top right):** mic gain and speaker volume. Leave
  **mic gain mostly alone** and control loudness with your voice and
  mic distance instead (Chapter 1).

## Recording your calibration test

Before your first real take, do this 2-minute ritual:

1. Set your mic distance to about 2–4 inches (5–10 cm), slightly off-axis
   (see Chapter 1).
2. Press Record and read *anything out loud for 30 seconds* — a paragraph
   from your book is ideal — starting after a two-second silent runway.
3. Press Stop. Look at your waveform.
4. **Aim for peaks hanging around the middle of the track height**, never
   touching the top or bottom lines. If you're in the middle now, good. If
   you're tiny, you can move closer to the mic or raise mic gain *a little*
   (you want headroom to stay under -3 dB peaks — Chapter 3 explains).
5. Plug in headphones and play it back. You should hear your room as
   *near-silence behind your voice*.

If peaks clip (touch the 0 dB top), lower your voice level to the mic —
pull back an inch or reduce mic gain — and retest. It's much easier to
quietly amplify soft audio in editing than to fix crackly clipped audio at
all.

## Saving and file organization

Audacity's project format (`.aup3`) stores everything, including your edits.
For the workflow in Chapter 5:

- Save an **Audacity project per chapter**: one file in a chapter folder,
  named like `ch07.aup3`.
- Record all your takes for that chapter in that one project, then edit and
  master there before exporting the final WAV.
- Exported WAV/MP3 files are *deliverables*, not working files; give them
  their own subfolder.

> **The one Audacity habit to build today:** press **Ctrl+S** after every
> take. Audacity has become stable over the years, but a power blink without
> a save has ruined enough narrator weekends that it deserves this bolded
> warning.

## Keyboard shortcuts worth memorizing

Five keys save you hundreds of hand-moves per chapter:

- **Spacebar:** play/stop
- **Shift+Space:** play from last cursor position (listen-back)
- **Ctrl+Z / Ctrl+Y:** undo/redo
- **Ctrl+S:** save (see above)
- **X / hold X:** (on a selection) Audacity's "zoom to selection" via View

That's genuinely all the interface you need. Everything fancier —
noise-reduction, compression, EQ, mastering — is covered in Chapter 3 with
exact plain-number recipes, and Chapter 5 puts it all in order.
