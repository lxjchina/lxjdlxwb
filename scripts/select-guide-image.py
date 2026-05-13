#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fast WorkBuddy guide image selector.

This script does not launch Chrome and has no third-party dependencies. It
selects one prebuilt 2x PNG from assets/ based on a topic or user text, then
verifies the PNG dimensions from the file header.
"""

import argparse
import json
import os
import struct
import sys


BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
MANIFEST = os.path.join(ROOT, "assets", "guide-images.json")


def load_manifest():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def png_size(path):
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    return struct.unpack(">II", header[16:24])


def normalize_topic(topic, manifest):
    if topic in manifest["topics"]:
        return topic
    return manifest["defaultTopic"]


def infer_topic(text, manifest):
    text = (text or "").strip().lower()
    if not text:
        return manifest["defaultTopic"]

    best_topic = manifest["defaultTopic"]
    best_score = 0
    for topic, data in manifest["topics"].items():
        score = 0
        for keyword in data.get("keywords", []):
            keyword = keyword.lower()
            if keyword and keyword in text:
                score += max(len(keyword), 1)
        if score > best_score:
            best_topic = topic
            best_score = score
    return best_topic


def resolve_image(topic, manifest):
    data = manifest["topics"][topic]
    rel_path = data["path"]
    abs_path = os.path.join(ROOT, rel_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(abs_path)

    width, height = png_size(abs_path)
    expected_width = int(manifest.get("quality", {}).get("width", 1360))
    if width < expected_width:
        raise ValueError(f"{rel_path} is {width}px wide, expected at least {expected_width}px")

    return {
        "topic": topic,
        "title": data["title"],
        "path": rel_path,
        "absolutePath": abs_path,
        "width": width,
        "height": height,
        "mode": manifest.get("imageMode", "prebuilt-assets-first"),
    }


def main():
    manifest = load_manifest()
    parser = argparse.ArgumentParser(description="快速选择 WorkBuddy 钓虾高清兜底图")
    parser.add_argument("--topic", choices=sorted(manifest["topics"].keys()), help="指定主题")
    parser.add_argument("--text", help="用户原始问题，用于自动判断主题")
    parser.add_argument("--json", action="store_true", help="输出 JSON，方便 WorkBuddy 读取")
    args = parser.parse_args()

    topic = normalize_topic(args.topic, manifest) if args.topic else infer_topic(args.text, manifest)
    result = resolve_image(topic, manifest)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["path"])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
