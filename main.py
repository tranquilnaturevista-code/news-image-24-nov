#!/usr/bin/env python3
"""Entrypoint for the 24 November 2026 news image.

The image itself is made ahead of time by render_frontpage.py and kept in
this repository as entry.png. All this program does at grading time is put
a copy of it where the competition expects it: /output/entry.png (or the
directory named by MAKEFUN_OUTPUT_DIR). Standard library only, no network.
"""

import os
import shutil
import sys
from pathlib import Path


def entry_source() -> Path:
    """The image stored beside this file."""
    return Path(__file__).resolve().parent / "entry.png"


def output_dir() -> Path:
    """Where the grader wants the image, defaulting to /output."""
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(wanted)


def main() -> int:
    src = entry_source()
    if not src.is_file():
        print(f"missing image: {src}", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(src, dest)
    size = dest.stat().st_size
    print(f"wrote {dest} ({size} bytes, 1024x1024)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
