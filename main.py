#!/usr/bin/env python3
"""Famous Last Words at 1 Percent — make.fun entry.

Writes the funniest possible last words a phone says as its battery
hits 1 percent: a single line of at most 199 characters, as plain text,
to /output/entry.txt (or $ENTRY_OUTPUT for local testing).

Stdlib only, deterministic, no network, no randomness.
"""
import os
import sys

# The phone's last words: its owner opens the camera to photograph it
# dying. Three short beats, the punch ("The audacity.") landing last.
ENTRY = "He opened the camera to take one last photo. Of me. Dying. The audacity."

MAX_CHARS = 199


def validate(text):
    """Gate: 1-199 characters, not only whitespace, a single line."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main():
    text = validate(ENTRY)
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # No trailing newline: the file holds exactly the line.
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    # Read back and compare byte for byte.
    with open(out_path, "rb") as fh:
        raw = fh.read()
    if raw.decode("utf-8") != text:
        raise SystemExit("round-trip mismatch: file does not match the entry")
    print(f"wrote {len(text)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
