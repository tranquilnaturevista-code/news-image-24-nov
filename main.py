#!/usr/bin/env python3
"""Publish the 24 November 2026 front page to the runner's output folder.

The finished page lives in this repository as ``entry.png`` — it was
drawn in this session by ``render_frontpage.py``. This script is only
the publisher: it reads that file, checks it is a complete PNG inside
the competition's limits (at most 1024x1024 pixels, at most 1 MiB), and
writes an exact copy to ``/output/entry.png`` (or to the directory named
by ``MAKEFUN_OUTPUT_DIR`` when that is set).

Nothing is re-encoded, resized, or redrawn, so the page the judge sees
is byte for byte the page that was laid out here. Only the Python
standard library is used and no network is touched.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DEFAULT_OUTPUT = "/output"
LIMIT_BYTES = 1_048_576
LIMIT_SIDE = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_TAIL = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def die(message):
    print(f"main.py: ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def inspect_png(path):
    """Return (size, width, height) of a PNG that passes every check."""
    data = path.read_bytes()
    if len(data) > LIMIT_BYTES:
        die(f"{path} is {len(data)} bytes, over the 1 MiB limit")
    if not data.startswith(PNG_SIGNATURE):
        die(f"{path} does not start with the PNG signature")
    if len(data) < 24 or data[12:16] != b"IHDR":
        die(f"{path} has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", data[16:24])
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        die(f"{path} is {width}x{height}, over the 1024x1024 limit")
    if not data.endswith(PNG_TAIL):
        die(f"{path} does not end with a proper IEND chunk")
    return len(data), width, height


def main():
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        die(f"cannot find {SOURCE_NAME} next to main.py")

    size, width, height = inspect_png(source)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / SOURCE_NAME
    shutil.copyfile(source, target)

    copied = target.stat().st_size
    if copied != size:
        die(f"copy is {copied} bytes but the source is {size} bytes")
    print(f"main.py: wrote {target} ({width}x{height}, {size} bytes)")


if __name__ == "__main__":
    main()
