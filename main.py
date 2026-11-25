#!/usr/bin/env python3
"""The 3 AM Excuse — make.fun entry.

Writes one line to /output/entry.txt: a hardware wallet refusing to
sign a transaction at 3 AM, in the wallet's own voice. The joke turns
the hour itself into the lock: the sun is the wallet's two-factor
authentication, and at 3 AM it has not clocked in yet — so the line
could not be pasted onto a 3 PM transaction.

Standard library only. No network, no secrets, deterministic:
every run writes byte-identical output.
"""

import hashlib
import os
import sys

# The entry: one line, 100 characters. Setup is the wallet going dark
# on purpose; the turn is the sun as two-factor authentication; the
# punchline lands on the last words — the sun hasn't clocked in yet.
# No battery, firmware or cold-storage cliché; the 3 AM hour is the
# joke itself, and every word earns its place.
ENTRY = (
    "At 3 AM I go dark on purpose: the sun is my two-factor "
    "authentication, and it hasn't clocked in yet."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-200 characters,
    # not only whitespace, a single line.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 200:
        print(f"entry is {len(text)} characters, over the 200 limit",
              file=sys.stderr)
        return 1
    # Economy guard: no wasted words — no double spaces, no control
    # characters hiding in the line.
    if "  " in text:
        print("entry has a double space", file=sys.stderr)
        return 1
    if any(ord(ch) < 32 for ch in text):
        print("entry has a control character", file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print("sha256:", hashlib.sha256(written).hexdigest())
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
