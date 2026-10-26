# Checklists

Print these. Tape them near your recording desk. They exist because your
brain stops helping at minute 40.

## One-time setup checklist

- [ ] Recording corner chosen (corner or closet; quiet side of the building)
- [ ] Blanket/drapes/towels cover previously-reflected surfaces (behind mic especially)
- [ ] Noise audit done (30-second silent listen at full volume helped identify any hums/wows)
- [ ] Culprit appliances/off-ending scheduled noted (fridge, AC, fans)
- [ ] Mic chosen and positioned 2–4 inches from mouth, slightly off-axis
- [ ] Foam windscreen or pop filter on the mic
- [ ] Headphones plugged in and set as playback device
- [ ] Audacity installed from audacityteam.org
- [ ] Audacity input/output devices set (named, not "default")
- [ ] Project rate = 44100 Hz, recording quality 32-bit float
- [ ] Software playthrough / overdub OFF
- [ ] Calibration test recorded: peaks float between the middle lines, never clipping
- [ ] Folder structure created (manuscript/, projects/, masters/, deliver/, pickup-notes/)
- [ ] LOG.md started
- [ ] Story: water, green apple, tissues, throat lozenges on the desk

## Per-chapter session checklist (start)

- [ ] Chapter pre-read done once, emphasis and pauses marked on paper copy
- [ ] Pronunciations for names/terms written directly on the page
- [ ] First 30 seconds of the room, full volume: confirm silence before starting
- [ ] New Audacity project opened (projects/chXX.aup3), 44100 Hz
- [ ] 5 seconds of room tone recorded first ("session tone")
- [ ] Session log line started in LOG.md
- [ ] Water within arm's reach
- [ ] Mic distance checked (2–4 inches) — same as last session

## Per-take checklist (during recording)

- [ ] Flub → 1-second pause → re-read from start of the phrase → keep going
- [ ] No "sorry", no dramatic sighs after takes
- [ ] Ctrl+S pressed after every take
- [ ] Room tone (2–3 seconds) recorded after a long break/splice point
- [ ] Session capped at 90 minutes (voice hygiene) — take a real break after

## Per-chapter (after recording) checklist

- [ ] Flubs cut (bridge from flub → end of clean re-read)
- [ ] Real silences trimmed below ~1.5 seconds (leave natural breaths)
- [ ] Loud late-line breaths trimmed around (word before not clipped)
- [ ] Room tone pasted under harsh splices that sound unsupported
- [ ] Session-tone strip removed from the chapter head
- [ ] Skim-listen at 1x for continuity before moving on
- [ ] Peaks amplified/limited to -3 dB max
- [ ] Loudness normalized to ~-19 LUFS (target window for mono audiobook)
- [ ] 3+ seconds room tone at head
- [ ] ~1 second room tone at tail
- [ ] WAV exported to masters/chXX-master.wav (44100 Hz, 32-bit float, mono)
- [ ] MP3 exported to deliver/ (constant 192 kbps, 44100 Hz, mono, sortable name)
- [ ] Project saved (Ctrl+S)
- [ ] LOG.md updated with done-line

## Delivery checklist (before uploading)

- [ ] Full listener pass done in order at 1x, all chapters
- [ ] Cross-session loudness sounds matched
- [ ] No chapter starts with trimmed-word-too-fast; ends with room tone
- [ ] File names zero-padded and sortable (e.g., 03_Cold_Evidence.mp3)
- [ ] Current store spec sheet re-checked at the source (do this right before spread/upload)
- [ ] Cover art ready (at least 1600×1600) at required store size
- [ ] Narrator field set ("Read by the author" if applicable)
- [ ] Master WAVs backed up somewhere off-disk (cloud/external drive)

## Pickup session checklist (small fixes)

- [ ] Fix *only* named items from the pickup-notes file
- [ ] New phrase recorded in same project, same mic distance
- [ ] Re-run master steps on affected chapter only
- [ ] Re-export WAV and MP3 (overwrite)
- [ ] Listen once to confirm the splice is invisible
