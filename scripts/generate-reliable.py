#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老乡农场钓虾教学图 - 可靠生成脚本
一键生成 + 自动验证 + 智能分割
使用方法: python generate-reliable.py [--split]
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """运行命令并返回结果"""
    print(f"\n{'='*50}")
    print(f"{description}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"警告: {result.stderr}")
    return result.returncode == 0

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("╔" + "="*48 + "╗")
    print("║" + " "*12 + "老乡农场钓虾教学图生成器" + " "*13 + "║")
    print("║" + " "*10 + "Reliable Edition v3.0" + " "*17 + "║")
    print("╚" + "="*48 + "╝")

    # 步骤 1: 生成图片
    if not run_command(
        f"cd '{base_dir}' && python3 generate-guide-v3.py",
        "步骤 1/3: 生成教学长图"
    ):
        print("\n✗ 图片生成失败，请检查错误信息")
        return 1

    # 步骤 2: 验证图片
    output_path = os.path.join(base_dir, "output", "diaoxiapu_guide_v3.png")
    if not os.path.exists(output_path):
        print(f"\n✗ 错误: 找不到生成的图片 {output_path}")
        return 1

    print(f"\n{'='*50}")
    print("步骤 2/3: 图片验证")
    print(f"{'='*50}")

    # 使用 PIL 验证
    try:
        from PIL import Image
        img = Image.open(output_path)
        print(f"✓ 图片验证通过")
        print(f"  尺寸: {img.size[0]}×{img.size[1]}px")
        print(f"  格式: {img.format}")
        print(f"  模式: {img.mode}")

        # 检查是否需要分割
        if img.height > 2000:
            print(f"\n⚠ 图片高度 {img.height}px 超过 2000px")
            print("  建议分割成多张图片以便微信分享")

            # 自动分割
            if "--split" in sys.argv or "--auto-split" in sys.argv:
                if not run_command(
                    f"cd '{base_dir}' && python3 split-long-image.py output/diaoxiapu_guide_v3.png output/split",
                    "步骤 3/3: 自动分割长图"
                ):
                    print("\n✗ 分割失败")
                    return 1
            else:
                print(f"\n提示: 添加 --split 参数可自动分割图片")
                print(f"  命令: python generate-reliable.py --split")

    except Exception as e:
        print(f"✗ 图片验证失败: {e}")
        return 1

    # 输出结果
    print(f"\n{'='*50}")
    print("生成完成!")
    print(f"{'='*50}")
    print(f"\n输出文件:")
    print(f"  长图: {output_path}")

    # 检查是否有分割后的图片
    split_dir = os.path.join(base_dir, "output", "split")
    if os.path.exists(split_dir):
        split_files = [f for f in os.listdir(split_dir) if f.endswith('.png')]
        if split_files:
            print(f"\n  分割图片 ({len(split_files)} 张):")
            for f in sorted(split_files):
                print(f"    - output/split/{f}")

    print(f"\n验证报告:")
    report_path = os.path.join(base_dir, "output", "validation_report.json")
    if os.path.exists(report_path):
        print(f"  - {report_path}")

    print(f"\n{'='*50}")
    print("✓ 所有步骤完成！")
    print(f"{'='*50}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
