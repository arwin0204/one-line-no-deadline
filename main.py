#!/usr/bin/env python3
"""One Line, No Deadline Met -- make.fun entry (program/v1).

Writes a single-line joke giving an excuse for a missed deadline to
/output/entry.txt (the make.fun program harness output path).

The entry is a fixed, hand-written one-liner. The program is fully
deterministic: no randomness, no clock, no network, no environment
input. Every run produces byte-identical output.

Gate (per RULES.txt): entry.txt must be UTF-8 text of 1 to 200
characters, not only white space. This program self-checks the gate
on every run and refuses to write an invalid entry.
"""

import os
import sys
from pathlib import Path

ENTRY = (
    "I didn't miss the deadline \u2014 I outsourced it to Future Me, "
    "and Future Me has been ghosting me for three weeks."
)

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 200


def validate_entry(text: str) -> None:
    """Enforce the competition gate before writing anything."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (GATE_MIN_CHARS <= len(text) <= GATE_MAX_CHARS):
        raise ValueError(
            "entry is %d characters, gate requires %d-%d"
            % (len(text), GATE_MIN_CHARS, GATE_MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text != text.strip():
        raise ValueError("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def output_path() -> Path:
    """Resolve where entry.txt goes.

    The grader runs the program with /output as the harness output
    directory. For local runs, pass a directory as argv[1] or set
    OUTPUT_DIR, so the file can be inspected without root access.
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1]) / "entry.txt"
    return Path(os.environ.get("OUTPUT_DIR", "/output")) / "entry.txt"


def main() -> int:
    if "--check-only" in sys.argv[1:]:
        validate_entry(ENTRY)
        print("gate OK: %d characters, single line" % len(ENTRY))
        return 0
    validate_entry(ENTRY)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write with a trailing newline: the file content is the entry
    # plus the conventional line terminator; the entry text itself
    # is one line and well inside the 200-character gate.
    path.write_text(ENTRY + "\n", encoding="utf-8")
    # Round-trip check: what was written must read back byte-exact
    # as the entry plus the single trailing newline.
    written = path.read_bytes()
    if written != (ENTRY + "\n").encode("utf-8"):
        raise ValueError("round-trip check failed: written bytes differ")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
