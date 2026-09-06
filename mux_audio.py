#!/usr/bin/env python3
"""Mux Scene-level add_sound() cues into their manim-slides slide clips.

manim only mixes accumulated add_sound() audio into the final combined
Deck.mp4/.wav (Scene.combine_to_movie); manim-slides instead concatenates
manim's per-play *partial movie files* directly, which never carry audio.
So every add_sound() cue is silently dropped from the exported slides.

This finds each cue's absolute scene-time (via silencedetect on Deck.wav,
in the same order add_sound() is called in deck.py) and mutes it back in
by muxing the original sound file into the target slide clip at the right
offset. Run after `manim-slides render`, before `manim-slides convert`.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DECK_JSON = ROOT / "slides" / "Deck.json"


def ffprobe_duration(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return float(out)
    except (subprocess.CalledProcessError, ValueError):
        return 0.0


def find_wav():
    candidates = list((ROOT / "media" / "videos" / "deck").glob("*/Deck.wav"))
    if not candidates:
        sys.exit("no Deck.wav found under media/videos/deck/*/ — run render first")
    # Name-sorting quality dirs is wrong ("1080p60" < "480p15" as strings),
    # so take whichever one was actually rendered most recently.
    return max(candidates, key=lambda p: p.stat().st_mtime)


def sound_onsets(wav):
    """Scene-time (seconds) each non-silent stretch begins, in order."""
    proc = subprocess.run(
        ["ffmpeg", "-i", str(wav), "-af", "silencedetect=noise=-40dB:d=0.05",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    return [float(m) for m in re.findall(r"silence_end: ([\d.]+)", proc.stderr)]


def sound_call_order():
    src = (ROOT / "deck.py").read_text()
    return re.findall(r"""self\.add_sound\(["'](.+?)["']\)""", src)


def main():
    wav = find_wav()
    onsets = sound_onsets(wav)
    calls = sound_call_order()
    if len(onsets) != len(calls):
        sys.exit(f"found {len(onsets)} sound events in Deck.wav but "
                  f"{len(calls)} add_sound() calls in deck.py — can't "
                  "match them up safely, aborting")
    if not onsets:
        print("no add_sound() cues, nothing to mux")
        return

    slides = json.loads(DECK_JSON.read_text())["slides"]
    durations = [ffprobe_duration(ROOT / s["file"]) for s in slides]

    # ponytail: this cumulative walk doesn't skip next_slide(src=...) slides,
    # which consume no Deck.wav scene-time (they're copied in raw, never
    # rendered by manim). Only correct as long as every add_sound() cue lands
    # before the first src= slide in the deck. Add src-slide detection if a
    # future cue needs to land after one.
    cursor = 0.0
    slide_i = 0
    for onset, wav_file in zip(onsets, calls):
        while slide_i < len(slides) - 1 and cursor + durations[slide_i] <= onset:
            cursor += durations[slide_i]
            slide_i += 1
        offset = onset - cursor
        target = ROOT / slides[slide_i]["file"]
        sound_path = ROOT / wav_file
        delay_ms = max(0, int(offset * 1000))
        tmp = target.with_suffix(".muxed.mp4")
        # ponytail: last cue wins if two cues land in the same slide clip.
        # Not the case today (3 cues, 3 distinct slides), revisit if it changes.
        subprocess.run([
            "ffmpeg", "-y", "-i", str(target), "-i", str(sound_path),
            "-filter_complex", f"[1:a]adelay={delay_ms}|{delay_ms}[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
            str(tmp),
        ], check=True, capture_output=True)
        tmp.replace(target)
        print(f"muxed {sound_path.name} into slide {slide_i} at +{offset:.2f}s")


if __name__ == "__main__":
    main()
