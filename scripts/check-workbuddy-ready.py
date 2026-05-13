#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check that the WorkBuddy skill can use all declared prebuilt PNG assets.

This is a lightweight readiness check for client/miniprogram delivery. It does
not require Chrome or Pillow.
"""

import json
import os
import struct
import sys


BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
MANIFEST = os.path.join(ROOT, "assets", "guide-images.json")


def png_size(path):
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    return struct.unpack(">II", header[16:24])


def main():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    expected_width = int(manifest.get("quality", {}).get("width", 1360))
    failures = []

    print("WorkBuddy readiness check")
    print("=" * 40)
    for topic, data in sorted(manifest.get("topics", {}).items()):
        rel_path = data.get("path", "")
        title = data.get("title", topic)
        abs_path = os.path.join(ROOT, rel_path)
        if not os.path.exists(abs_path):
            failures.append(f"{topic}: missing {rel_path}")
            print(f"✗ {topic} {title}: missing {rel_path}")
            continue
        try:
            width, height = png_size(abs_path)
        except Exception as exc:
            failures.append(f"{topic}: invalid PNG: {exc}")
            print(f"✗ {topic} {title}: invalid PNG: {exc}")
            continue
        if width < expected_width:
            failures.append(f"{topic}: width {width}px < {expected_width}px")
            print(f"✗ {topic} {title}: {width}x{height}, too narrow")
            continue
        print(f"✓ {topic} {title}: {width}x{height} {rel_path}")

    print("=" * 40)
    if failures:
        print(f"FAILED: {len(failures)} issue(s)")
        return 1

    print("READY: all declared WorkBuddy PNG assets are available")
    return 0


if __name__ == "__main__":
    sys.exit(main())
