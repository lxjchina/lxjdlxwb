#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 钓虾教学图资源校验。

校验目标：
- HTML 不引用外部或本地图片，所有图片必须是 data:image/png;base64。
- base64 图片能被解码，避免小程序端缺 logo 或空图。
- PNG 输出足够清晰，不是空白图。
"""

import argparse
import base64
import os
import re
import sys
from html.parser import HTMLParser


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            self.images.append(attrs)
        if "href" in attrs:
            self.hrefs.append(attrs["href"])


def fail(message, failures):
    print(f"✗ {message}")
    failures.append(message)


def ok(message):
    print(f"✓ {message}")


def validate_html(path):
    failures = []
    if not os.path.exists(path):
        fail(f"HTML 文件不存在: {path}", failures)
        return failures

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    parser = AssetParser()
    parser.feed(html)

    if not parser.images:
        fail("HTML 中没有找到任何 <img>，请确认 logo 是否被误删", failures)
    else:
        ok(f"找到 {len(parser.images)} 个图片元素")

    for index, img in enumerate(parser.images, start=1):
        src = img.get("src", "")
        alt = img.get("alt", f"image-{index}")
        if not src.startswith("data:image/png;base64,"):
            fail(f"图片 {index}({alt}) 不是内联 PNG data URI", failures)
            continue
        payload = src.split(",", 1)[1]
        try:
            decoded = base64.b64decode(payload, validate=True)
        except Exception as exc:
            fail(f"图片 {index}({alt}) base64 解码失败: {exc}", failures)
            continue
        if len(decoded) < 1024:
            fail(f"图片 {index}({alt}) 数据过小，可能是空图", failures)
        else:
            ok(f"图片 {index}({alt}) 已内联，{len(decoded) / 1024:.1f} KB")

    external_patterns = [
        r"<script\b[^>]*\bsrc=",
        r"<link\b[^>]*\bhref=",
        r"url\((?!['\"]?data:)",
        r"src=['\"](?:https?:|file:|\.\.?/|/)",
    ]
    for pattern in external_patterns:
        if re.search(pattern, html, flags=re.IGNORECASE):
            fail(f"发现外部或本地资源引用: {pattern}", failures)

    html_without_data = re.sub(
        r"data:image/[^;]+;base64,[A-Za-z0-9+/=]+",
        "data:image/png;base64,<inline-image>",
        html,
        flags=re.IGNORECASE,
    )
    placeholders = ["TODO", "TBD", "{{", "}}", "__"]
    for token in placeholders:
        if token in html_without_data:
            fail(f"发现未替换占位符: {token}", failures)

    if not failures:
        ok("HTML 资源校验通过：可在 WorkBuddy 小程序里作为自包含预览源使用")
    return failures


def validate_png(path):
    failures = []
    if not path:
        return failures
    if not os.path.exists(path):
        fail(f"PNG 文件不存在: {path}", failures)
        return failures

    try:
        from PIL import Image, ImageStat
    except Exception as exc:
        fail(f"未安装 Pillow，无法校验 PNG: {exc}", failures)
        return failures

    img = Image.open(path).convert("RGB")
    width, height = img.size
    if width < 1360:
        fail(f"PNG 宽度 {width}px 偏低，WorkBuddy 需要 2x 高清图（至少 1360px 宽）", failures)
    else:
        ok(f"PNG 宽度 {width}px，满足高清展示")

    if height < 1000:
        fail(f"PNG 高度 {height}px 过低，可能没有截完整", failures)
    else:
        ok(f"PNG 高度 {height}px")

    stat = ImageStat.Stat(img.resize((max(width // 12, 1), max(height // 12, 1))))
    channel_ranges = [hi - lo for lo, hi in stat.extrema]
    if max(channel_ranges) < 30:
        fail("PNG 色彩变化过小，疑似空白或缺元素", failures)
    else:
        ok("PNG 非空白，色彩层次正常")

    file_size = os.path.getsize(path)
    if file_size < 200 * 1024:
        fail(f"PNG 文件仅 {file_size / 1024:.1f} KB，可能导出不完整", failures)
    else:
        ok(f"PNG 文件大小 {file_size / 1024:.1f} KB")

    if not failures:
        ok("PNG 输出校验通过：清晰度和完整性达标")
    return failures


def main():
    parser = argparse.ArgumentParser(description="校验 WorkBuddy 钓虾教学 HTML/PNG 资源")
    parser.add_argument("html", help="要校验的 HTML 文件")
    parser.add_argument("png", nargs="?", help="可选：要校验的 PNG 文件")
    args = parser.parse_args()

    print("WorkBuddy 资源校验")
    print("=" * 40)
    failures = []
    failures.extend(validate_html(args.html))
    if args.png:
        print("-" * 40)
        failures.extend(validate_png(args.png))

    if failures:
        print("=" * 40)
        print(f"校验失败：{len(failures)} 个问题")
        return 1

    print("=" * 40)
    print("全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
