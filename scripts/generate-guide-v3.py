#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老乡农场钓虾教学长图生成器 v3.0 - 可靠版
- 预检查所有资源
- 详细的错误报告
- 图片验证
- 分割长图选项
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import sys
import json
from datetime import datetime

# ── 配置 ──────────────────────────────────────────
W = 680
PAD = 24
MAX_SINGLE_IMAGE_HEIGHT = 2000  # 微信建议单图最大高度

# ── 路径 ──────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

# ── 验证报告 ──────────────────────────────────────
validation_report = {
    "timestamp": datetime.now().isoformat(),
    "checks": [],
    "errors": [],
    "warnings": [],
    "output_files": []
}

def log_check(name, status, detail=""):
    validation_report["checks"].append({"name": name, "status": status, "detail": detail})
    icon = "✓" if status == "pass" else "⚠" if status == "warn" else "✗"
    print(f"  {icon} {name}: {detail}")

def log_error(msg):
    validation_report["errors"].append(msg)
    print(f"  ✗ 错误: {msg}")

def log_warning(msg):
    validation_report["warnings"].append(msg)
    print(f"  ⚠ 警告: {msg}")

# ── 1. 预检查 ─────────────────────────────────────
print("=" * 50)
print("步骤 1/4: 预检查资源")
print("=" * 50)

# 检查字体
FONT_PATHS = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]
FONT_VALID = None
for fp in FONT_PATHS:
    if os.path.exists(fp):
        FONT_VALID = fp
        log_check("中文字体", "pass", fp)
        break
if not FONT_VALID:
    log_error("未找到中文字体")
    sys.exit(1)

# 测试字体加载
try:
    test_font = ImageFont.truetype(FONT_VALID, 14)
    log_check("字体加载测试", "pass")
except Exception as e:
    log_error(f"字体加载失败: {e}")
    sys.exit(1)

def font(size):
    try:
        return ImageFont.truetype(FONT_VALID, size)
    except Exception as e:
        log_warning(f"字体大小 {size} 加载失败，使用默认字体")
        return ImageFont.load_default()

# 检查 Logo 文件
LOGO_DIR = os.path.dirname(BASE)
LOGO_FILES = {
    "wk": "WK.png",
    "lxj": "老乡农场 logo.png",
    "farm": "老乡农场 logo.png"
}
LOGO = {}
for key, filename in LOGO_FILES.items():
    fp = os.path.join(LOGO_DIR, filename)
    if os.path.exists(fp):
        try:
            LOGO[key] = Image.open(fp)
            log_check(f"Logo [{key}]", "pass", filename)
        except Exception as e:
            log_warning(f"Logo [{key}] 加载失败: {e}")
    else:
        log_warning(f"Logo [{key}] 未找到: {filename}")

if not LOGO:
    log_warning("未找到任何 Logo 文件，将生成无 Logo 版本")

# ── 颜色 ──────────────────────────────────────────
C = {
    "green":   (0x00, 0x80, 0x42),
    "green_d": (0x00, 0x66, 0x34),
    "gold":    (0xFF, 0xC5, 0x20),
    "gold_d":  (0xFF, 0x8A, 0x00),
    "bg":      (0xE9, 0xDB, 0xCC),
    "white":   (255, 255, 255),
    "black":   (0x23, 0x18, 0x15),
    "gray":    (0x55, 0x55, 0x55),
    "gray_l":  (0xBB, 0xBB, 0xBB),
    "red":     (0xE4, 0x38, 0x28),
    "cream":   (0xF8, 0xF5, 0xF0),
    "warn_bg": (0xFF, 0xF8, 0xE7),
    "warn_bd": (0xFF, 0xC5, 0x20),
    "safe":    (0xF0, 0xF8, 0xF4),
    "danger":  (0xFF, 0xF0, 0xF0),
}

cur_y = [0]
img = None
draw = None

def init_canvas():
    global img, draw
    img = Image.new("RGB", (W, 6000), C["bg"])
    draw = ImageDraw.Draw(img)

# ── 工具函数 ──────────────────────────────────────
def fill_rounded(draw, xy, r, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1+r, y1, x2-r, y2], fill=fill)
    draw.rectangle([x1, y1+r, x2, y2-r], fill=fill)
    draw.pieslice([x1, y1, x1+2*r, y1+2*r], 180, 270, fill=fill)
    draw.pieslice([x2-2*r, y1, x2, y1+2*r], 270, 360, fill=fill)
    draw.pieslice([x1, y2-2*r, x1+2*r, y2], 90, 180, fill=fill)
    draw.pieslice([x2-2*r, y2-2*r, x2, y2], 0, 90, fill=fill)

def draw_logo(img, logo_key, xy, max_sz=40):
    """在 img 上绘制 logo，自动缩放到 max_sz 高度"""
    if logo_key not in LOGO:
        return xy[0], xy[1]
    logo = LOGO[logo_key]
    ratio = min(max_sz / logo.height, max_sz / logo.width)
    new_w, new_h = int(logo.width * ratio), int(logo.height * ratio)
    logo_r = logo.resize((new_w, new_h), Image.LANCZOS)
    x, y = xy
    try:
        if logo_r.mode == 'RGBA':
            img.paste(logo_r, (x, y), logo_r)
        else:
            img.paste(logo_r, (x, y))
    except Exception as e:
        log_warning(f"Logo 粘贴失败: {e}")
    return x, y

def draw_text(draw, pos, text, size, color=None, anchor="la"):
    x, y = pos
    f = font(size)
    try:
        draw.text((x, y), text, font=f, fill=color or C["black"], anchor=anchor)
    except Exception as e:
        log_warning(f"文字渲染失败 '{text[:20]}...': {e}")

def section_gap():
    cur_y[0] += 12

# ── 绘制函数 ──────────────────────────────────────
def draw_header():
    y = cur_y[0]
    draw.rectangle([0, y, W, y + 110], fill=C["green"])
    draw.ellipse([-40, y + 90, W + 40, y + 170], fill=C["white"])
    if "farm" in LOGO:
        draw_logo(img, "farm", (PAD, y + 10), 50)
    if "lxj" in LOGO:
        draw_logo(img, "lxj", (W - PAD - 50, y + 10), 50)
    draw_text(draw, (W//2, y + 36), "老乡农场钓虾指南", 20, color=C["white"], anchor="mm")
    draw_text(draw, (W//2, y + 70), "鸡肠子才是 yyds！", 14, color=C["gold"], anchor="mm")
    cur_y[0] = y + 115

def draw_env_banner():
    y = cur_y[0]
    x1, x2 = PAD, W - PAD
    h = 80
    fill_rounded(draw, [x1, y, x2, y+h], 12, C["green"])
    draw_text(draw, (x1+20, y+h//2), "沟渠宽1.6米 深50cm | 鸡肠子饵料", 14, color=C["white"], anchor="lm")
    cur_y[0] = y + h + 16

def draw_section_title(text, num=None):
    y = cur_y[0]
    if num is not None:
        cx, cy = PAD + 14, y + 14
        draw.ellipse([cx-14, cy-14, cx+14, cy+14], fill=C["green"])
        draw_text(draw, (cx, cy), str(num), 14, color=C["white"], anchor="mm")
        tx = PAD + 38
    else:
        tx = PAD
    draw_text(draw, (tx, y+2), text, 20, color=C["green"])
    cur_y[0] = y + 38
    section_gap()

def draw_equipment():
    y = cur_y[0]
    items = [
        ("钓竿", "2-3米竹竿"), ("钓线", "尼龙线1.5-2米"),
        ("钓钩", "6-8号虾钩"), ("鸡肠子", "新鲜"),
        ("水桶", "带盖塑料桶"), ("抄网", "直径20-30cm"),
        ("折叠凳", "久站不累"), ("小剪刀", "处理饵料"),
    ]
    col_w = (W - PAD*2 - 8) // 2
    row_h = 52
    for i, (name, desc) in enumerate(items):
        col = i % 2
        row = i // 2
        x1 = PAD + col * (col_w + 8)
        y1 = y + row * (row_h + 8)
        x2 = x1 + col_w
        y2 = y1 + row_h
        fill_rounded(draw, [x1, y1, x2, y2], 8, C["cream"])
        draw_text(draw, (x1+8, y1+6), name, 13, color=C["black"])
        draw_text(draw, (x1+8, y1+28), desc, 11, color=C["gray"])
    cur_y[0] = y + ((len(items)+1)//2) * (row_h+8) + 8

def draw_bait():
    y = cur_y[0]
    x1, x2 = PAD, W-PAD
    h = 140
    draw.rectangle([x1, y, x2, y+h], fill=C["warn_bg"], outline=C["gold"], width=2)
    draw_text(draw, (x1+14, y+12), "鸡肠子处理四步法", 15, color=(0x8B,0x69,0x14))
    steps = ["1. 清洗：清水冲洗2-3遍", "2. 切割：剪成3-5cm小段",
             "3. 穿钩：钩尖微露1-2mm", "4. 现用：20分钟换一轮"]
    for i, s in enumerate(steps):
        draw_text(draw, (x1+14, y+42+i*20), s, 13, color=C["black"])
    draw.rectangle([x1+10, y+h-32, x2-10, y+h-8], fill=C["white"])
    draw_text(draw, (x1+18, y+h-30), "增强秘诀：穿好钩后滴1-2滴香油，效果翻倍！", 11, color=C["green"])
    cur_y[0] = y + h + 16

def draw_position():
    y = cur_y[0]
    items = [
        ("首选：水草丰茂处", "水草边缘内侧10-20cm是黄金落点"),
        ("沟渠拐角处", "水流变缓，食物沉积，内弯处更优"),
        ("阴凉暗处/进水口", "溶氧高、食物多，虾聚集")
    ]
    for title, body in items:
        y1 = cur_y[0]
        h = 76
        fill_rounded(draw, [PAD, y1, W-PAD, y1+h], 10, C["cream"])
        draw.rectangle([PAD, y1, PAD+4, y1+h], fill=C["green"])
        draw_text(draw, (PAD+14, y1+8), title, 14, color=C["black"])
        draw_text(draw, (PAD+14, y1+34), body, 12, color=C["gray"])
        cur_y[0] = y1 + h + 10
    cur_y[0] += 6

def draw_signal_table():
    y = cur_y[0]
    rows = [
        ("探测期", "线微微抖动", "不动", C["gray_l"]),
        ("夹持期", "线被缓慢拉紧", "再等1-2秒", C["gold"]),
        ("吞食期", "线突然被快速拖入水中", "立即提竿", C["red"])
    ]
    col1, col2 = 220, 340
    row_h = 48
    draw.rectangle([PAD, y, W-PAD, y+32], fill=C["green"])
    draw_text(draw, (PAD+8, y+6), "阶段", 13, color=C["white"])
    draw_text(draw, (PAD+90+8, y+6), "信号", 13, color=C["white"])
    draw_text(draw, (PAD+col2+8, y+6), "操作", 13, color=C["white"])
    cur_y[0] = y + 32
    for i, (stage, sig, op, clr) in enumerate(rows):
        y1 = cur_y[0]
        bg = C["cream"] if i%2==0 else C["white"]
        draw.rectangle([PAD, y1, W-PAD, y1+row_h], fill=bg)
        draw_text(draw, (PAD+8, y1+8), stage, 13, color=clr)
        draw_text(draw, (PAD+90+8, y1+8), sig, 12, color=C["black"])
        draw_text(draw, (PAD+col2+8, y1+8), op, 12, color=clr)
        cur_y[0] = y1 + row_h
    draw.rectangle([PAD, cur_y[0], W-PAD, cur_y[0]+40], fill=C["warn_bg"])
    draw.rectangle([PAD, cur_y[0], PAD+4, cur_y[0]+40], fill=C["gold"])
    draw_text(draw, (W//2, cur_y[0]+20), "抖不动，走再等，跑就提", 16,
              color=(0x8B,0x69,0x14), anchor="mm")
    cur_y[0] += 48

def draw_lift():
    y = cur_y[0]
    steps = [
        ("1", "确认信号", "线在跑而非抖，确认虾已吞饵"),
        ("2", "手腕上扬", "手腕发力快速上弹30-45度，不要猛甩"),
        ("3", "匀速收线", "感觉到重量后匀速收线，不要急拽"),
        ("4", "抄网接住", "虾接近水面时用抄网从下方接住")
    ]
    for num, title, body in steps:
        y1 = cur_y[0]
        h = 70
        fill_rounded(draw, [PAD, y1, W-PAD, y1+h], 10, C["cream"])
        draw.ellipse([PAD+8, y1+14, PAD+36, y1+42], fill=C["green"])
        draw_text(draw, (PAD+22, y1+28), num, 14, color=C["white"], anchor="mm")
        draw_text(draw, (PAD+48, y1+10), title, 14, color=C["black"])
        draw_text(draw, (PAD+48, y1+36), body, 12, color=C["gray"])
        cur_y[0] = y1 + h + 10
    draw.rectangle([PAD, cur_y[0], W-PAD, cur_y[0]+36], fill=C["danger"])
    draw.rectangle([PAD, cur_y[0], PAD+4, cur_y[0]+36], fill=C["red"])
    draw_text(draw, (PAD+12, cur_y[0]+4), "摘钩安全：从虾背部中段捏住，避开两只大钳！", 12, color=C["red"])
    draw_text(draw, (PAD+12, cur_y[0]+22), "被夹了别甩手，放水里虾会松开。", 12, color=C["red"])
    cur_y[0] += 44

def draw_time_chart():
    y = cur_y[0]
    draw_text(draw, (PAD, y), "最佳垂钓时间", 18, color=C["green"])
    cur_y[0] = y + 30
    times = [
        ("5:00-7:00", 100, "极佳·虾最活跃", C["gold"]),
        ("7:00-9:00", 85, "很好", C["green"]),
        ("9:00-11:00", 55, "一般", (0xBF,0xB0,0x8F)),
        ("11:00-15:00", 30, "较差·避开", (0xBF,0xB0,0x8F)),
        ("15:00-17:00", 100, "极佳·黄金时段！", C["gold"]),
        ("17:00-19:00", 85, "很好", C["green"]),
        ("19:00-21:00", 70, "不错", C["green"])
    ]
    bar_max_w = W - PAD*2 - 90 - 10
    for label, pct, desc, clr in times:
        y1 = cur_y[0]
        draw_text(draw, (PAD, y1+2), label, 12, color=C["gray"])
        bw = int(bar_max_w * pct / 100)
        fill_rounded(draw, [PAD+90, y1, PAD+90+bw, y1+22], 6, clr)
        draw_text(draw, (PAD+98, y1+3), desc, 11, color=C["white"])
        cur_y[0] = y1 + 30
    draw.rectangle([PAD, cur_y[0], W-PAD, cur_y[0]+36], fill=C["safe"])
    draw.rectangle([PAD, cur_y[0], PAD+4, cur_y[0]+36], fill=C["green"])
    draw_text(draw, (PAD+12, cur_y[0]+4), "农场推荐时段：15:00-17:00", 13, color=C["green"])
    draw_text(draw, (PAD+12, cur_y[0]+22), "光线好、温度适宜、体验最佳！", 12, color=C["green"])
    cur_y[0] += 44

def draw_mnemonic():
    y = cur_y[0]
    fill_rounded(draw, [PAD, y, W-PAD, y+260], 14, C["green_d"])
    draw_text(draw, (W//2, y+18), "钓虾七字诀", 19, color=C["white"], anchor="mm")
    grid_x = [PAD+6, PAD+6+(W-PAD*2-12)//2]
    grid_w = (W-PAD*2-12)//2
    grid_h = 60
    chars = [
        ("站", "选位站草边 轻手又轻脚"), ("抛", "饵抛草边落 宁近不要远"),
        ("等", "线抖不要急 线跑再出手"), ("提", "巧劲向上抖 匀速慢慢收"),
        ("抄", "虾露快下网 千万别手抓"), ("摘", "背后来下手 安全记心间"),
        ("养", "桶中加浅水 盖紧防逃跑")
    ]
    for i, (ch, txt) in enumerate(chars):
        col = i % 2
        r = i // 2
        x1 = grid_x[col]
        y1 = y + 50 + r * (grid_h+6)
        draw.rectangle([x1, y1, x1+grid_w, y1+grid_h], fill=(50,120,80))
        draw_text(draw, (x1+grid_w//2, y1+14), ch, 24, color=C["gold"], anchor="mm")
        draw_text(draw, (x1+grid_w//2, y1+40), txt, 11, color=C["white"], anchor="mm")
    draw_text(draw, (W//2, y+240), "洗两遍，剪三段，钩尖微露最划算", 13, color=C["gold"], anchor="mm")
    cur_y[0] = y + 268

def draw_faq():
    y = cur_y[0]
    draw_text(draw, (PAD, y), "常见问题", 18, color=C["green"])
    cur_y[0] = y + 30
    faqs = [
        ("为什么别人钓了很多，我一上午没钓到？", "①位置不对②时间不对③动作太大④饵料问题"),
        ("饵料总被吃光但钓不到虾？", "虾太小、钩太大。换小号钩+小段饵料"),
        ("一有动静就提竿，总是空钩？", "太早了！记住：抖不动，走再等，跑就提"),
        ("下雨天能钓吗？", "小雨天更好！暴雨天别去，安全第一")
    ]
    for q, a in faqs:
        y1 = cur_y[0]
        draw_text(draw, (PAD, y1), q, 13, color=C["green"])
        q_h = 20
        a_lines = textwrap.wrap(a, width=38)
        a_h = len(a_lines) * 20 + 8
        for line in a_lines:
            draw_text(draw, (PAD, y1+q_h), line, 12, color=C["gray"])
        cur_y[0] = y1 + q_h + a_h + 10
    cur_y[0] += 4

def draw_safety():
    y = cur_y[0]
    col_w = (W - PAD*2 - 8) // 2
    x1 = PAD
    draw.rectangle([x1, y, x1+col_w, y+180], outline=C["green"], width=2)
    draw.rectangle([x1, y, x1+col_w, y+32], fill=C["green"])
    draw_text(draw, (x1+col_w//2, y+16), "请这样做", 14, color=C["white"], anchor="mm")
    for i, item in enumerate(["穿防滑鞋", "大人陪同", "带走垃圾", "太小的虾放生", "适量获取"]):
        draw_text(draw, (x1+22, y+40+i*26), f"✔ {item}", 12, color=C["green"])
    x2 = PAD + col_w + 8
    draw.rectangle([x2, y, x2+col_w, y+180], outline=C["red"], width=2)
    draw.rectangle([x2, y, x2+col_w, y+32], fill=C["red"])
    draw_text(draw, (x2+col_w//2, y+16), "不要这样", 14, color=C["white"], anchor="mm")
    for i, item in enumerate(["站陡坡边缘", "雷雨天出去", "丢物品入渠", "使用化学诱饵", "破坏水草"]):
        draw_text(draw, (x2+22, y+40+i*26), f"✘ {item}", 12, color=C["red"])
    cur_y[0] = y + 188

def draw_footer():
    y = cur_y[0] + 12
    draw.rectangle([0, y, W, y+90], fill=C["green"])
    draw.rectangle([W//2-30, y+55, W//2+30, y+58], fill=C["gold"])
    if "wk" in LOGO:
        draw_logo(img, "wk", (W//2+40, y+10), 40)
    draw_text(draw, (W//2, y+20), "老乡鸡", 18, color=C["white"], anchor="mm")
    draw_text(draw, (W//2, y+44), "鸡肠子配小龙虾，老乡鸡的浪漫", 13, color=(200,255,200), anchor="mm")
    draw_text(draw, (W//2, y+66), "WorkBuddy AI 生成 · 老乡农场专用", 11,
              color=(180,255,180), anchor="mm")
    cur_y[0] = y + 95

# ── 主流程 ────────────────────────────────────────
print("\n" + "=" * 50)
print("步骤 2/4: 生成图片内容")
print("=" * 50)

init_canvas()
cur_y[0] = 0

# 绘制所有内容
draw_header()
draw_env_banner()
section_gap()
draw_section_title("准备钓具", 1)
draw_equipment()
section_gap()
draw_section_title("处理鸡肠子饵料", 2)
draw_bait()
section_gap()
draw_section_title("选对钓位", 3)
draw_position()
section_gap()
draw_section_title("投饵等待 · 感知信号", 4)
draw_signal_table()
section_gap()
draw_section_title("提竿抄虾", 5)
draw_lift()
section_gap()
draw_time_chart()
section_gap()
draw_mnemonic()
section_gap()
draw_section_title("常见问题", None)
draw_faq()
section_gap()
draw_safety()
section_gap()
draw_footer()

# ── 裁切和保存 ────────────────────────────────────
print("\n" + "=" * 50)
print("步骤 3/4: 保存和验证")
print("=" * 50)

final_h = cur_y[0] + 20
img_cropped = img.crop((0, 0, W, final_h))

output_path = os.path.join(OUT_DIR, "diaoxiapu_guide_v3.png")
img_cropped.save(output_path, "PNG", optimize=True)
validation_report["output_files"].append(output_path)
log_check("图片保存", "pass", output_path)

# 验证生成的图片
print("\n验证生成的图片...")
try:
    verify_img = Image.open(output_path)
    log_check("图片可读性", "pass", f"{verify_img.size[0]}×{verify_img.size[1]}px")

    # 检查尺寸
    if verify_img.height > MAX_SINGLE_IMAGE_HEIGHT:
        log_warning(f"图片高度 {verify_img.height}px 超过微信建议值 {MAX_SINGLE_IMAGE_HEIGHT}px")
        log_warning("建议：考虑分割成多张图片")

    # 检查文件大小
    file_size = os.path.getsize(output_path)
    log_check("文件大小", "pass", f"{file_size/1024:.1f} KB")

    if file_size > 2 * 1024 * 1024:
        log_warning("文件超过 2MB，可能影响微信分享")

except Exception as e:
    log_error(f"图片验证失败: {e}")

# ── 保存验证报告 ──────────────────────────────────
report_path = os.path.join(OUT_DIR, "validation_report.json")
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(validation_report, f, ensure_ascii=False, indent=2)

# ── 输出摘要 ──────────────────────────────────────
print("\n" + "=" * 50)
print("步骤 4/4: 生成摘要")
print("=" * 50)

print(f"\n✓ 图片生成完成")
print(f"  输出路径: {output_path}")
print(f"  图片尺寸: {W}×{final_h}px")
print(f"  验证报告: {report_path}")

if validation_report["errors"]:
    print(f"\n✗ 发现 {len(validation_report['errors'])} 个错误")
    for e in validation_report["errors"]:
        print(f"    - {e}")

if validation_report["warnings"]:
    print(f"\n⚠ 发现 {len(validation_report['warnings'])} 个警告")
    for w in validation_report["warnings"]:
        print(f"    - {w}")

print("\n" + "=" * 50)
print("生成完成！")
print("=" * 50)
