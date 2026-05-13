#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 转 PNG 工具 - Chrome Headless 版
将 WorkBuddy 自包含 HTML 转为高清 PNG 图片。

用法:
    python3 html-to-png.py <html_file> [output.png]
    python3 html-to-png.py generate-fishing-guide.html output/workbuddy-fishing-guide@2x.png
    python3 html-to-png.py topic-html/full.html output/fishing-guide@2x.png --scale 2
"""

import os
import sys
import subprocess
import argparse

DEFAULT_WIDTH = 680
DEFAULT_HEIGHT = 12000
DEFAULT_SCALE = 2


def get_chrome_path():
    """查找 Chrome 可执行文件"""
    possible_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def crop_blank_bottom(output_path):
    """裁掉截图底部的空白视口，保留完整卡片内容。"""
    try:
        from PIL import Image
    except Exception:
        print("   ⚠️  未安装 Pillow，跳过底部空白裁切")
        return

    img = Image.open(output_path).convert("RGB")
    width, height = img.size
    bg = img.getpixel((max(width - 2, 0), max(height - 2, 0)))
    threshold = 18
    last_content_row = height - 1

    for y in range(height - 1, -1, -1):
        samples = [img.getpixel((x, y)) for x in range(0, width, max(width // 40, 1))]
        changed = 0
        for px in samples:
            if sum(abs(px[i] - bg[i]) for i in range(3)) > threshold:
                changed += 1
        if changed >= max(2, len(samples) // 12):
            last_content_row = y
            break

    crop_bottom = min(height, last_content_row + 24)
    if crop_bottom < height - 32:
        img.crop((0, 0, width, crop_bottom)).save(output_path, "PNG", optimize=True)
        print(f"   ✂️  已裁切底部空白: {width} x {crop_bottom}px")


def html_to_png(html_path, output_path=None, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, scale=DEFAULT_SCALE):
    """将 HTML 文件转换为 PNG（完整页面截图）"""
    chrome = get_chrome_path()
    if not chrome:
        print("❌ 错误：未找到 Chrome 浏览器")
        print("   请安装 Google Chrome 或 Chromium")
        return False

    if not os.path.exists(html_path):
        print(f"❌ 错误：文件不存在 {html_path}")
        return False

    # 确定输出路径
    if output_path is None:
        base = os.path.splitext(html_path)[0]
        output_path = f"{base}.png"

    # 确保输出目录存在
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print(f"🖼️  正在转换: {html_path}")
    print(f"   Chrome: {chrome}")
    print(f"   画布: {width} x {height} CSS px @ {scale}x")

    try:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--single-process",
            "--hide-scrollbars",
            "--disable-features=IsolateOrigins,site-per-process",
            "--run-all-compositor-stages-before-draw",
            "--disable-font-subpixel-positioning",
            f"--force-device-scale-factor={scale}",
            f"--window-size={width},{height}",
            "--virtual-time-budget=3000",
            f"--screenshot={os.path.abspath(output_path)}",
            f"file://{os.path.abspath(html_path)}",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)

        if os.path.exists(output_path):
            crop_blank_bottom(output_path)
            size = os.path.getsize(output_path)
            print(f"✅ 成功: {output_path}")
            print(f"   大小: {size / 1024:.1f} KB")
            return True
        else:
            print(f"❌ 截图失败")
            if result.stderr:
                print(f"   错误: {result.stderr[:300]}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ 错误：Chrome 截图超时")
        return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False


def batch_convert(input_dir, output_dir=None):
    """批量转换目录中的所有 HTML 文件"""
    if output_dir is None:
        output_dir = os.path.join(input_dir, "..", "png-output")

    os.makedirs(output_dir, exist_ok=True)

    html_files = [f for f in os.listdir(input_dir) if f.endswith(".html")]

    if not html_files:
        print(f"⚠️  目录中没有 HTML 文件: {input_dir}")
        return

    print(f"📁 批量转换 {len(html_files)} 个文件...")
    print(f"   输入: {input_dir}")
    print(f"   输出: {output_dir}")
    print()

    success_count = 0
    for html_file in sorted(html_files):
        html_path = os.path.join(input_dir, html_file)
        output_path = os.path.join(output_dir, html_file.replace(".html", "@2x.png"))
        if html_to_png(html_path, output_path):
            success_count += 1
        print()

    print(f"✅ 完成: {success_count}/{len(html_files)} 个文件转换成功")


def main():
    parser = argparse.ArgumentParser(description="将 WorkBuddy 自包含 HTML 转成高清 PNG")
    parser.add_argument("html_path", nargs="?", help="输入 HTML 文件")
    parser.add_argument("output_path", nargs="?", help="输出 PNG 文件")
    parser.add_argument("--batch", action="store_true", help="批量转换目录下的 HTML")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="CSS 视口宽度，默认 680")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="CSS 视口高度，默认 12000")
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE, choices=[1, 2, 3], help="设备像素倍率，默认 2")
    args = parser.parse_args()

    if args.batch:
        input_dir = args.html_path if args.html_path else "topic-html"
        batch_convert(input_dir)
    else:
        if not args.html_path:
            parser.print_help()
            sys.exit(1)
        html_to_png(args.html_path, args.output_path, args.width, args.height, args.scale)


if __name__ == "__main__":
    main()
