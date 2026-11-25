"""One Line, No Deadline Met — entry writer.

Reads the single excuse line from ``entry.txt`` (kept beside this script),
validates it against the bounty gate (1-200 characters, non-blank), writes
it to the harness output path, and prints it to stdout.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.txt"
DEFAULT_OUTPUT = Path("/output/entry.txt")

MAX_CHARS = 200


def load_line(source: Path) -> str:
    """Return the excuse line, stripped of surrounding whitespace."""
    text = source.read_text(encoding="utf-8")
    line = text.strip()
    if not line:
        raise ValueError(f"{source} is empty")
    if len(line) > MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, over the {MAX_CHARS} cap")
    if "\n" in line:
        raise ValueError("entry must be a single line")
    return line


def write_entry(line: str, destination: Path) -> Path:
    """Write the line to *destination*, creating parent dirs as needed."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(line + "\n", encoding="utf-8")
    return destination


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    output = Path(args[0]) if args else DEFAULT_OUTPUT
    try:
        line = load_line(SOURCE)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    try:
        write_entry(line, output)
    except OSError:
        # No harness output dir (e.g. a local run): fall back beside the script.
        output = HERE / "entry-output.txt"
        try:
            write_entry(line, output)
        except OSError as exc:
            print(f"error: cannot write output: {exc}", file=sys.stderr)
            return 1
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
