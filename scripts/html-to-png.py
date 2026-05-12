#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML 转 PNG 工具 - Chrome Headless 版
无损将 HTML 页面转换为高清 PNG 图片（完整页面截图）

用法:
    python3 html-to-png.py <html_file> [output.png]
    python3 html-to-png.py topic-html/bait.html
    python3 html-to-png.py topic-html/full.html output/fishing-guide.png
"""

import os
import sys
import subprocess
import tempfile
import json
import time


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


def get_page_height(chrome, html_path):
    """使用 Chrome 获取页面的实际滚动高度"""
    js_file = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False)
    js_file.write("""
        const result = {
            width: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth),
            height: Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)
        };
        console.log('DIMENSIONS:' + JSON.stringify(result));
    """)
    js_file.close()

    try:
        result = subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--virtual-time-budget=3000",
                "--run-all-compositor-stages-before-draw",
                f"--inject-javascript={js_file.name}",
                f"file://{os.path.abspath(html_path)}",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        # 从 stderr 中解析维度信息
        for line in result.stderr.split('\n'):
            if 'DIMENSIONS:' in line:
                json_str = line.split('DIMENSIONS:')[1]
                dims = json.loads(json_str)
                return dims

        # 如果解析失败，返回默认值
        return {"width": 680, "height": 1200}
    except Exception:
        return {"width": 680, "height": 1200}
    finally:
        os.unlink(js_file.name)


def html_to_png(html_path, output_path=None):
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

    # 第一步：获取页面实际高度
    print("   📏 测量页面高度...")
    dims = get_page_height(chrome, html_path)
    page_height = dims.get("height", 1200)
    print(f"   页面尺寸: 680 x {page_height}px")

    # 第二步：用足够大的窗口截图，确保捕获完整页面
    # Chrome 的 --screenshot 会截取当前视口，我们需要设置窗口高度 >= 页面高度
    window_height = max(page_height + 100, 800)

    try:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--disable-features=IsolateOrigins,site-per-process",
            f"--window-size=680,{window_height}",
            "--virtual-time-budget=3000",
            "--run-all-compositor-stages-before-draw",
            f"--screenshot={os.path.abspath(output_path)}",
            f"file://{os.path.abspath(html_path)}",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if os.path.exists(output_path):
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
        output_path = os.path.join(output_dir, html_file.replace(".html", ".png"))
        if html_to_png(html_path, output_path):
            success_count += 1
        print()

    print(f"✅ 完成: {success_count}/{len(html_files)} 个文件转换成功")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n示例:")
        print("  python3 html-to-png.py topic-html/bait.html")
        print("  python3 html-to-png.py topic-html/full.html output/guide.png")
        print("  python3 html-to-png.py --batch topic-html/")
        sys.exit(1)

    if sys.argv[1] == "--batch":
        input_dir = sys.argv[2] if len(sys.argv) > 2 else "topic-html"
        batch_convert(input_dir)
    else:
        html_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        html_to_png(html_path, output_path)


if __name__ == "__main__":
    main()
