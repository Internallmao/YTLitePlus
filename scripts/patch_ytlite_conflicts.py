#!/usr/bin/env python3
"""Patch YTLite dylib conflict-name strings to avoid false-positive tweak warnings.

This rewrites only fixed-length ASCII substrings in-place.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPLACEMENTS = {
    b"YTLitePlus.dylib": b"YTLitePluz.dylib",
    b"uYou.dylib": b"uY0u.dylib",
    b"uYouPlus.dylib": b"uYouPluz.dylib",
    b"iSponsorBlock.dylib": b"iSp0nsorBlock.dylib",
    b"DLTube.dylib": b"DLTuba.dylib",
    b"DLYouTube.dylib": b"DLY0uTube.dylib",
    b"YouTubeReborn.dylib": b"YouTubeReb0rn.dylib",
    b"uYouEnhanced.dylib": b"uYouEnhanc3d.dylib",
    b"YouTimeStamp.dylib": b"YouTimeSt4mp.dylib",
    b"YTRebornObjc.dylib": b"YTReborn0bjc.dylib",
}


def patch_file(path: Path) -> int:
    blob = path.read_bytes()
    total_replacements = 0

    for old, new in REPLACEMENTS.items():
        if len(old) != len(new):
            raise ValueError(f"Replacement length mismatch: {old!r} -> {new!r}")
        count = blob.count(old)
        if count:
            blob = blob.replace(old, new)
            total_replacements += count
            print(f"patched {old.decode()} -> {new.decode()} ({count}x)")

    if total_replacements:
        path.write_bytes(blob)
    else:
        print("no known conflict strings found to patch")

    return total_replacements


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dylib", type=Path)
    args = parser.parse_args()

    if not args.dylib.exists():
        print(f"error: file not found: {args.dylib}", file=sys.stderr)
        return 1

    patch_file(args.dylib)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
