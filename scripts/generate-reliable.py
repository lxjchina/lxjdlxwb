#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老乡农场钓虾教学图 - WorkBuddy 可靠生成脚本
一键校验 HTML、生成 2x PNG、再校验 PNG 完整性。
使用方法:
  python3 generate-reliable.py
  python3 generate-reliable.py --topic bait
"""

import argparse
import subprocess
import sys
import os

TOPICS = {
    "full": "完整指南",
    "equipment": "装备准备",
    "bait": "鸡肠子饵料",
    "position": "钓位选择",
    "signal": "咬钩信号",
    "lift": "提竿抄虾",
    "time": "最佳时间",
    "mnemonic": "钓虾口诀",
    "safety": "安全提醒",
}

def run_command(cmd, description):
    """运行命令并返回结果"""
    print(f"\n{'='*50}")
    print(f"{description}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"警告: {result.stderr}")
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="生成 WorkBuddy 钓虾高清图")
    parser.add_argument(
        "--topic",
        default="full",
        choices=sorted(TOPICS.keys()),
        help="按用户问题生成对应主题图",
    )
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("╔" + "="*48 + "╗")
    print("║" + " "*12 + "老乡农场钓虾教学图生成器" + " "*13 + "║")
    print("║" + " "*8 + "WorkBuddy Reliable Edition" + " "*13 + "║")
    print("╚" + "="*48 + "╝")

    html_path = os.path.join(base_dir, "generate-fishing-guide.html")
    suffix = "" if args.topic == "full" else f"-{args.topic}"
    output_path = os.path.join(base_dir, "output", f"workbuddy-fishing-guide{suffix}@2x.png")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 步骤 0: 根据主题重建 HTML
    if not run_command(
        [
            sys.executable,
            os.path.join(base_dir, "build-workbuddy-guide.py"),
            "--topic",
            args.topic,
            "--output",
            html_path,
        ],
        f"步骤 0/3: 生成 HTML 模板（{TOPICS[args.topic]}）"
    ):
        print("\n✗ HTML 模板生成失败，请检查错误信息")
        return 1

    # 步骤 1: 校验 HTML 资源
    if not run_command(
        [sys.executable, os.path.join(base_dir, "validate-workbuddy-assets.py"), html_path],
        "步骤 1/3: 校验 WorkBuddy HTML 资源"
    ):
        print("\n✗ HTML 资源校验失败，请检查错误信息")
        return 1

    # 步骤 2: 高清导出 PNG
    if not run_command(
        [sys.executable, os.path.join(base_dir, "html-to-png.py"), html_path, output_path, "--scale", "2"],
        "步骤 2/3: 生成高清 PNG"
    ):
        print("\n✗ PNG 生成失败，请检查 Chrome 或 HTML 模板")
        return 1

    # 步骤 3: 校验 PNG 清晰度与完整性
    if not run_command(
        [sys.executable, os.path.join(base_dir, "validate-workbuddy-assets.py"), html_path, output_path],
        "步骤 3/3: 校验高清 PNG"
    ):
        print("\n✗ PNG 校验失败，请检查导出结果")
        return 1

    # 输出结果
    print(f"\n{'='*50}")
    print("生成完成!")
    print(f"{'='*50}")
    print(f"\n输出文件:")
    print(f"  主题: {TOPICS[args.topic]} ({args.topic})")
    print(f"  WorkBuddy 高清图: {output_path}")

    print(f"\n{'='*50}")
    print("✓ 所有步骤完成！")
    print(f"{'='*50}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
