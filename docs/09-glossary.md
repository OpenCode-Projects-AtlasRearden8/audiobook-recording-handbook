# Glossary

Every technical term used in this handbook, in plain English. If a word
here is still confusing in a sentence, that's a handbook bug — tell us.

### ACX
Audiobook Creation eXchange — Amazon and Audible's program and platform
for producing and distributing audiobooks. Even though stores keep
changing, its audio quality checklist is the de-facto "strict bar" that
audio engineers and home studios both target.

### Amplify
An Audacity effect that raises or lowers the whole audio by the same
number of decibels. Used in mastering to set the file's peak to a target
level.

### Bit depth
How precisely each audio sample is measured. 32-bit float is generous and
protects you from making little mistakes permanent; 16-bit is CD-grade
and fine.

### Bit rate (kbps)
How many bits per second an MP3 uses. **Constant 192 kbps (or higher)** is
the audiobook spec — lower rates make speech sound swishy and metallic.

### Clipping
What audio sounds like when the level exceeds the digital ceiling: harsh,
crackly distortion. Cannot be reliably repaired. Prevented by leaving 3 dB
of headroom (peaks below -3 dB).

### Constant Bit Rate (CBR)
MP3 encoding mode where the file uses the same bit rate throughout. The
audiobook stores ask for CBR (rather than VBR) because it guarantees the
item is measured uniformly for every player-syncing service.

### Condenser mic
A type of microphone that is very sensitive — which in an untreated room
means "records the room and its problems." A dynamic mic is usually the
right choice for your bedroom chapter booth.

### dB (decibel)
The unit audio levels are measured in. 0 dB is the digital ceiling
(loud, where clipping happens); quieter levels are negative numbers. A
room-quiet recording measuring around -60 dB under speech at -20 dB is
'exactly what you want'.

### Dynamic microphone
A mic that hears a narrower "window" of sound than a condenser mic. The
right tool for an untreated bedroom: it hears more you, less room.

### Early reflections
The first, quick versions of your voice that bounce off nearby walls and
arrive at the mic slightly late. They're what makes a bedroom recording
sound "boxy." Blankets absorb them.

### Finished hour (PFH)
An hour of final, publishable audio. Narrator prices are quoted "Per
Finished Hour" (PFH). Your 90,000-word book is about a finished hour per
9,000 words — so a typical fiction book is roughly 7–10 finished hours.

### Headroom
The unused space between your loudest peak and the digital ceiling. You
want exactly 3 dB of it (-3 dB peak).

### Loudness normalization
An automatic process that raises/lowers the whole file so its *average
perceived loudness* (measured in LUFS) hits a target. Different from
"Amplify", which targets the peak instead.

### LUFS
Loudness Units relative to Full Scale — the way modern audio measures
perceived loudness. Audiobook specs are given in RMS decibels (below), and
LUFS and RMS line closely. A single ~-19 LUFS mono target lands your file
inside the required -18 to -23 dB RMS window.

### Mono
One audio channel. All audiobook store specs want mono — a podcaster's
"stereo" file actually delivers the same voice on both ears. Set it once
in the project.

### MP3
The compressed audio format stores require for delivery. 192 kbps
constant mono at 44100 Hz is the standard delivery profile.

### Noise floor
The constant background level of a recording when nobody is speaking:
your room's hum and the mic's self-noise together. Target: **at or below
-60 dB RMS**.

### Peak
The single loudest instant in a file, shown as the tallest part of the
waveform. The audiobook peak spec: -3 dB, never higher.

### Pop filter / windscreen
Foam or mesh on the mic that softens "P" and "B" breath bursts. Costs
almost nothing, prevents cartoonish pops.

### Project rate / Sample rate
How many audio "snapshots" per second a file stores. **44100 Hz (44.1
kHz)** is the CD standard and the audiobook spec. Set it in Audacity's
project bar bottom-right once.

### Reflection
Sound from your voice bouncing off a hard surface. Reflections are
the enemy; blankets are their natural predator.

### Reverb
The smeared tail of reflections in a room, like a bathroom echo, but on a
smaller scale. Fully desirable in a concert hall; fully undesirable at
2 a.m. in your recording booth.

### RMS
Root Mean Square — the "average loudness" of a passage. The audiobook
spec window: **-23 to -18 dB RMS**. Where peak shows the loudest instant,
RMS describes how loud the *steady voice* is.

### Room tone
The sound of your room while nothing is happening — technically, the same
"silence" a listener hears between sentences. Stores want 1–5 seconds at
the head and a second at the tail of each file, which also gives your own
edits something clean to splice from.

### Spec sheet
The store's written list of technical file requirements. Chapter 3
translates the common one into plain numbers.

### USB microphone
A mic that plugs in directly to your computer. Perfectly publishable for
audiobooks at the $50–$120 range, especially dynamic USB models.

### VBR (variable bit rate)
MP3 encoding that shifts bit rate based on the sound. Fine for music, not
what audiobook specs ask for — use Constant.

### Waveform
The visual squiggle for your audio in an editor. Taller = louder. Flat
= silence (or room tone). Your flub-finding in Chapter 5 lives here.
