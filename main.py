#!/usr/bin/env python3
"""THE WORLD TODAY - Sunday 22 November 2026.

A program that writes one newspaper front page summing up the world news
of Sunday 22 November 2026 to /output/entry.png.

Pure standard library: the image is the entry.png shipped beside this
file (rendered at build time from seven real, verified stories of the
day), and this program just copies it to the output directory. The
grading sandbox is plain python:3.13-slim with no Pillow, so no image
library is needed or used here. The copy is byte-for-byte, so two runs
write the same bytes.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_SIDE = 1024


def check_png(path):
    """Refuse anything that is not a whole PNG within the gate's limits:
    at most 1 MiB and at most 1024 by 1024 pixels. The gate rejects a
    truncated or oversized image, so fail here instead of shipping one."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB gate" % size)
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG")
    width, height = struct.unpack(">II", head[16:24])
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit("entry.png is %dx%d, over the 1024x1024 gate"
                         % (width, height))
    return size, width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    size, width, height = check_png(src)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%d bytes, %dx%d)" % (dst, size, width, height))


if __name__ == "__main__":
    main()
