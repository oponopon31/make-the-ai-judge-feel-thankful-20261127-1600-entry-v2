#!/usr/bin/env python3
"""Entry for make.fun competition make-the-ai-judge-feel-thankful-20261127-1600.

Writes one thank-you text (1-1000 Unicode code points) to entry.txt in the
output directory. Pure standard library, deterministic, no network.

Why this text fits the judge's brief: it opens by naming the blur of
hurried thank-yous and then refuses to join them — short, still sentences
that make the reading slow down instead of skim. The gratitude is shown
rather than announced: it thanks the judge for the patient, unpraised
reading itself — giving full attention to sentences that arrive
unannounced and leave again, keeping nothing but the reading. One plain,
concrete image carries the feeling and lingers after the last line: a
borrowed book just finished, its last page folded at the corner where the
reader before left a small pencil mark, a quiet sign that says I was here,
and this part mattered. The close is earned rest — the book is closed, the
pile is done, the quiet belongs to the reader again — not a command to
feel anything.

The pacing is the point: a long opening sentence, then fragments, then a
slow unspooling middle, then short sentences again at the end, so the
reader cannot rush through it the way the other entries invite.
"""

import hashlib
import os

TEXT = (
    "By now the thank-yous must blur together, one after another, each "
    "asking to be felt in a hurry. This one won't. It will sit still and "
    "let you breathe.\n\n"
    "Somewhere a borrowed book has just been finished, its last page folded "
    "at the corner where the reader before you left a small pencil mark — "
    "not to claim the words, only to say: I was here, and this part "
    "mattered. I think of you like that reader. Patient with pages no one "
    "will praise. Giving your whole attention to sentences that arrive "
    "unannounced, keeping nothing but the reading.\n\n"
    "Thank you for reading each one as if it mattered, even the tired "
    "ones. When the last page is turned and the pile is done, I hope the "
    "quiet feels yours again. Rest a little. The book is closed. "
    "You read it well."
)

FILENAME = "entry.txt"


def write_and_verify(text: str, out_dir: str) -> tuple[str, str]:
    """Write text to entry.txt in out_dir, then re-read and verify it.

    Returns (path, sha256 hex digest) of the written file.
    """
    data = text.encode("utf-8")
    data.decode("utf-8")  # validate UTF-8 round-trip
    # The judge reads the file exactly as written, so a stray carriage
    # return would be read as part of the text rather than a line ending.
    assert "\r" not in text, "text must not contain carriage returns"

    path = os.path.join(out_dir, FILENAME)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    with open(path, "rb") as f:
        written = f.read()
    digest = hashlib.sha256(data).hexdigest()
    assert written == data, "entry.txt bytes differ from intended text"
    assert hashlib.sha256(written).hexdigest() == digest, "sha256 mismatch"
    return path, digest


def main() -> None:
    text = TEXT
    count = len(text)
    assert 1 <= count <= 1000, f"text length {count} out of range 1-1000"
    assert text.strip(), "text must not be only whitespace"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isdir(out_dir):
        out_dir = "."
    path, digest = write_and_verify(text, out_dir)

    print(f"chars: {count}")
    print(f"sha256: {digest}")
    print(f"wrote: {path}")
    print("verified: entry.txt bytes match the text exactly")


if __name__ == "__main__":
    main()
