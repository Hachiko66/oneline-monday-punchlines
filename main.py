#!/usr/bin/env python3
"""Monday Morning Punchlines — one original joke about Monday mornings.

Writes a single fixed joke line to entry.txt. The joke is constant:
no randomness, no clock, no input, so every run is byte-identical.

The joke: the weekend as a subscription whose free trial just expired —
a fresh angle on Monday mornings, with the turn landing on the last
two words (the trial "auto-renews into work").
"""

import os
import sys

JOKE = "Monday morning: the weekend's free trial expired, and it auto-renews into work."

OUTPUT_FILENAME = "entry.txt"
MAX_CHARS = 200


def resolve_output_dir() -> str:
    """Where entry.txt goes: MAKEFUN_OUTPUT_DIR, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def validate_joke(line: str) -> None:
    """Gate rules: 1-200 chars, a single non-blank line, UTF-8 encodable."""
    if not line.strip():
        raise ValueError("joke must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("joke must be a single line")
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(f"joke must be 1-{MAX_CHARS} chars, got {len(line)}")
    line.encode("utf-8")  # raises if the text is not valid UTF-8


def write_entry(target: str, line: str) -> bytes:
    """Write the joke plus a trailing newline; force mode 0644.

    A 0600 mode once got an entry rejected, so the mode is set
    explicitly after writing instead of relying on the umask.
    """
    payload = (line + "\n").encode("utf-8")
    with open(target, "wb") as f:
        f.write(payload)
    os.chmod(target, 0o644)
    return payload


def verify_entry(target: str, expected: bytes) -> None:
    """Read the file back and prove it is byte-identical to the payload."""
    with open(target, "rb") as f:
        actual = f.read()
    if actual != expected:
        raise AssertionError("entry.txt does not match the joke payload")
    mode = os.stat(target).st_mode & 0o777
    if mode != 0o644:
        raise AssertionError(f"entry.txt mode is {oct(mode)}, expected 0o644")


def main() -> int:
    validate_joke(JOKE)
    output_dir = resolve_output_dir()
    os.makedirs(output_dir, exist_ok=True)
    target = os.path.join(output_dir, OUTPUT_FILENAME)
    payload = write_entry(target, JOKE)
    verify_entry(target, payload)
    print(f"Wrote {len(JOKE)}-character joke to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
