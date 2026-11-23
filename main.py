#!/usr/bin/env python3
"""One Sentence, One Journey — make.fun entry.

Writes a single one-sentence story about a journey to entry.txt inside
MAKEFUN_OUTPUT_DIR (default /output).

The story was written fresh for this contest, chosen from 12 original
candidates by a pairwise tournament scored against the published judge
brief, then tightened in a second revision pass (see ../variants.md).

Standard library only. No network, no files outside the output directory,
no environment assumptions beyond MAKEFUN_OUTPUT_DIR.
"""

import os
import sys

STORY = (
    "When the bridge washed out, the schoolteacher carried her pupils "
    "across the river on her back one by one, and the last child she "
    "carried grew up to be the engineer who rebuilt it thirty years later."
)

MAX_CHARS = 300
TERMINATORS = ".!?"


def validate(text):
    """Fail loudly if the text breaks the contest gate.

    Gate: UTF-8 text of 1 to 300 characters, not only whitespace, exactly
    one sentence, no title, no second sentence.
    """
    if not text or not text.strip():
        raise ValueError("entry is empty or whitespace only")
    if len(text) != len(text.strip()):
        raise ValueError("entry has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line (no newline characters)")
    # Exactly one sentence: exactly one sentence-terminating mark, and it
    # must be the final character, so there is no title and no second
    # sentence hiding in front of or behind it.
    marks = [ch for ch in text if ch in TERMINATORS]
    if len(marks) != 1:
        raise ValueError(
            "entry must contain exactly one sentence terminator, found %d"
            % len(marks)
        )
    if text[-1] not in TERMINATORS:
        raise ValueError("entry must end with its single sentence terminator")
    # UTF-8 round-trip: the gate reads the file as UTF-8.
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    text = validate(STORY)
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, "entry.txt")
    # Atomic write: temp file in the same directory, then replace.
    tmp = target + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.replace(tmp, target)
    print("wrote %s (%d characters, 1 sentence)" % (target, len(text)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        sys.exit(1)
