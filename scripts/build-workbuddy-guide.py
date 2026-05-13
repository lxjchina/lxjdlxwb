#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the WorkBuddy fishing guide HTML.

The output is a single self-contained HTML file with inline logo images, so
WorkBuddy mini-program previews and Chrome screenshots do not depend on local
image paths.
"""

import base64
import argparse
import os


BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
OUT = os.path.join(BASE, "generate-fishing-guide.html")
FARM_LOGO = os.path.join(ROOT, "老乡农场 logo.png")
WB_LOGO = os.path.join(ROOT, "WK.png")

TOPICS = {
    "full": {
        "title": "钓虾<br>看这张就够了",
        "subtitle": "1.6 米窄沟、50cm 浅水，重点不是猛甩，是找草边、稳住线、等它跑。",
        "points": [("草边", "落点 10-20cm"), ("鸡肠", "现穿现用"), ("跑提", "别急别猛")],
    },
    "equipment": {
        "title": "装备<br>轻巧就够了",
        "subtitle": "老乡农场窄沟不用长竿，1-1.5 米短竿更稳，配短线、虾钩和抄网就能开钓。",
        "points": [("短竿", "1-1.5米"), ("短线", "1.2-1.8米"), ("抄网", "出水接住")],
    },
    "bait": {
        "title": "鸡肠子<br>这样用最诱虾",
        "subtitle": "保留腥味、现穿现用、20 分钟没口就换。饵料新鲜，比复杂技巧更重要。",
        "points": [("清洗", "去杂留腥"), ("穿钩", "钩尖微露"), ("加香", "气味扩散")],
    },
    "position": {
        "title": "钓位<br>先找藏身处",
        "subtitle": "水草边、沟渠拐角、阴凉暗处，是小龙虾更愿意停留和觅食的位置。",
        "points": [("水草", "首选"), ("拐角", "聚食物"), ("阴影", "更安全")],
    },
    "signal": {
        "title": "咬钩<br>别提早",
        "subtitle": "线微抖先别动，线走慢再等一等，线快跑才提。空钩多半是太急。",
        "points": [("抖", "不动"), ("走", "再等"), ("跑", "就提")],
    },
    "lift": {
        "title": "提竿<br>稳比猛重要",
        "subtitle": "确认线在跑，再用手腕上扬 30-45°，有重量后匀速收线，快出水时用抄网接。",
        "points": [("确认", "线在跑"), ("上扬", "30-45°"), ("抄网", "下方接")],
    },
    "time": {
        "title": "时间<br>选对更好钓",
        "subtitle": "清晨和 15:00-17:00 都很好。农场推荐下午黄金档，光线和温度更适合观察。",
        "points": [("清晨", "很活跃"), ("下午", "黄金档"), ("正午", "少钓")],
    },
    "mnemonic": {
        "title": "口诀<br>一眼记住",
        "subtitle": "站、抛、等、提、抄、摘、养，把动作拆成 7 个字，新手也能快速上手。",
        "points": [("站", "轻手脚"), ("等", "线跑提"), ("养", "盖紧桶")],
    },
    "safety": {
        "title": "安全<br>玩得开心也要稳",
        "subtitle": "穿防滑鞋，孩子要有大人陪同；不手抓大钳，不雷雨天钓，不破坏沟渠环境。",
        "points": [("防滑", "不站陡坡"), ("陪同", "亲子必看"), ("环保", "带走垃圾")],
    },
}


def image_data(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def build_html(topic="full"):
    if topic not in TOPICS:
        raise ValueError(f"Unknown topic: {topic}")
    topic_data = TOPICS[topic]
    farm_logo = image_data(FARM_LOGO)
    wb_logo = image_data(WB_LOGO)
    hero_points = "\n".join(
        f'          <div class="hero-point"><strong>{title}</strong><span>{subtitle}</span></div>'
        for title, subtitle in topic_data["points"]
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>老乡农场钓虾指南</title>
<style>
  * {{ box-sizing: border-box; }}
  :root {{
    --green: #008042;
    --green-dark: #005f33;
    --leaf: #12a46b;
    --mint: #e9f8ef;
    --gold: #ffc520;
    --orange: #ff8a00;
    --red: #e43828;
    --water: #2da9e9;
    --water-soft: #e9f7ff;
    --rice: #fff8e9;
    --field: #f3e5c7;
    --paper: #fffdf6;
    --ink: #231815;
    --muted: #6f6259;
    --line: #eadcc2;
  }}
  body {{
    margin: 0;
    background: var(--field);
    color: var(--ink);
    font-family: "Source Han Sans CN", "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  }}
  .poster {{
    width: 680px;
    margin: 0 auto;
    overflow: hidden;
    background:
      linear-gradient(90deg, rgba(0,128,66,.045) 1px, transparent 1px),
      linear-gradient(180deg, rgba(0,128,66,.035) 1px, transparent 1px),
      var(--rice);
    background-size: 28px 28px;
  }}
  .hero {{
    position: relative;
    padding: 30px 30px 24px;
    color: #fff;
    background:
      linear-gradient(135deg, rgba(255,197,32,.95) 0 18%, transparent 18% 100%),
      linear-gradient(145deg, #006d3b 0%, #008042 46%, #13a06b 100%);
    border-bottom: 8px solid var(--gold);
  }}
  .hero::after {{
    content: "";
    position: absolute;
    left: -40px;
    right: -40px;
    bottom: -34px;
    height: 62px;
    background: var(--rice);
    transform: rotate(-2.5deg);
  }}
  .brand-row {{
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    width: max-content;
    max-width: 100%;
    margin: 0 auto 24px;
    padding: 8px 14px;
    background: rgba(255,255,255,.94);
    border-radius: 999px;
    box-shadow: 0 8px 20px rgba(0,0,0,.16);
  }}
  .brand-row img {{ display: block; height: 28px; width: auto; }}
  .brand-row .wb-logo {{ height: 24px; }}
  .brand-divider {{ width: 1px; height: 24px; background: #d4d0c8; }}
  .hero-grid {{
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: 1.08fr .92fr;
    gap: 20px;
    align-items: stretch;
  }}
  .eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(35,24,21,.24);
    color: #fff5d3;
    font-size: 14px;
    font-weight: 800;
  }}
  h1 {{
    margin: 14px 0 8px;
    font-size: 46px;
    line-height: 1.02;
    font-weight: 950;
    letter-spacing: 0;
  }}
  .subtitle {{
    margin: 0;
    font-size: 19px;
    line-height: 1.55;
    color: rgba(255,255,255,.92);
    font-weight: 650;
  }}
  .hero-points {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 18px;
  }}
  .hero-point {{
    padding: 12px 8px;
    border: 1px solid rgba(255,255,255,.3);
    border-radius: 12px;
    background: rgba(255,255,255,.16);
    text-align: center;
    backdrop-filter: blur(4px);
  }}
  .hero-point strong {{
    display: block;
    color: var(--gold);
    font-size: 22px;
    line-height: 1.1;
    font-weight: 950;
  }}
  .hero-point span {{
    display: block;
    margin-top: 4px;
    color: rgba(255,255,255,.92);
    font-size: 12px;
    font-weight: 800;
  }}
  .canal-card {{
    position: relative;
    min-height: 268px;
    border: 2px solid rgba(255,255,255,.45);
    border-radius: 22px;
    background: linear-gradient(180deg, rgba(255,255,255,.18), rgba(255,255,255,.08));
    overflow: hidden;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.18);
  }}
  .sun-label {{
    position: absolute;
    top: 18px;
    right: 18px;
    padding: 8px 10px;
    border-radius: 10px;
    background: var(--gold);
    color: #6a3d00;
    font-size: 13px;
    font-weight: 950;
    box-shadow: 0 8px 16px rgba(0,0,0,.15);
  }}
  .grass {{
    position: absolute;
    left: 18px;
    bottom: 42px;
    width: 112px;
    height: 122px;
  }}
  .blade {{
    position: absolute;
    bottom: 0;
    width: 10px;
    border-radius: 10px 10px 0 0;
    background: #6dcc57;
    transform-origin: bottom center;
  }}
  .blade:nth-child(1) {{ height: 82px; left: 8px; transform: rotate(-20deg); }}
  .blade:nth-child(2) {{ height: 110px; left: 24px; transform: rotate(-9deg); background: #a1d85d; }}
  .blade:nth-child(3) {{ height: 96px; left: 42px; transform: rotate(7deg); }}
  .blade:nth-child(4) {{ height: 120px; left: 60px; transform: rotate(18deg); background: #7bc957; }}
  .blade:nth-child(5) {{ height: 86px; left: 78px; transform: rotate(28deg); }}
  .water {{
    position: absolute;
    left: 82px;
    right: -30px;
    bottom: 36px;
    height: 112px;
    border-radius: 56px 0 0 56px;
    background:
      repeating-linear-gradient(170deg, rgba(255,255,255,.18) 0 10px, transparent 10px 28px),
      linear-gradient(90deg, #35bde7, #1387c5);
    box-shadow: inset 0 12px 24px rgba(255,255,255,.18), inset 0 -10px 20px rgba(0,70,110,.28);
  }}
  .line-stick {{
    position: absolute;
    left: 152px;
    top: 42px;
    width: 124px;
    height: 8px;
    border-radius: 99px;
    background: #87512d;
    transform: rotate(24deg);
    transform-origin: left center;
  }}
  .fishing-line {{
    position: absolute;
    left: 255px;
    top: 86px;
    width: 2px;
    height: 104px;
    background: rgba(255,255,255,.8);
    transform: rotate(7deg);
  }}
  .bait-dot {{
    position: absolute;
    right: 10px;
    top: 172px;
    padding: 7px 10px;
    border-radius: 999px;
    background: var(--red);
    color: #fff;
    font-size: 12px;
    font-weight: 950;
    white-space: nowrap;
    z-index: 5;
    box-shadow: 0 6px 14px rgba(160,20,10,.35);
  }}
  .cray {{
    position: absolute;
    right: 28px;
    bottom: 56px;
    width: 74px;
    height: 44px;
    border-radius: 42px 42px 32px 32px;
    background: linear-gradient(135deg, #e43828, #a91614);
    box-shadow: 0 8px 14px rgba(0,0,0,.18);
    z-index: 2;
  }}
  .cray::before, .cray::after {{
    content: "";
    position: absolute;
    top: -15px;
    width: 31px;
    height: 24px;
    border: 8px solid #d9231c;
    border-bottom: 0;
    border-radius: 24px 24px 0 0;
  }}
  .cray::before {{ left: -18px; transform: rotate(-28deg); }}
  .cray::after {{ right: -18px; transform: rotate(28deg); }}
  .dimension {{
    position: absolute;
    left: 28px;
    bottom: 14px;
    right: 28px;
    display: flex;
    justify-content: space-between;
    gap: 8px;
  }}
  .dimension span {{
    flex: 1;
    padding: 8px 6px;
    border-radius: 10px;
    background: rgba(255,255,255,.9);
    color: var(--green-dark);
    text-align: center;
    font-size: 13px;
    font-weight: 950;
  }}
  .section {{
    position: relative;
    padding: 28px 26px 0;
  }}
  .section:first-of-type {{ padding-top: 44px; }}
  .section-head {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
  }}
  .num {{
    display: grid;
    place-items: center;
    width: 34px;
    height: 34px;
    border-radius: 12px;
    background: var(--green);
    color: #fff;
    font-size: 17px;
    font-weight: 950;
    box-shadow: 0 7px 13px rgba(0,128,66,.22);
  }}
  h2 {{
    margin: 0;
    font-size: 26px;
    line-height: 1.15;
    font-weight: 950;
    letter-spacing: 0;
  }}
  .section-kicker {{
    margin-left: auto;
    padding: 7px 10px;
    border-radius: 999px;
    background: #fff;
    color: var(--muted);
    border: 1px solid var(--line);
    font-size: 12px;
    font-weight: 850;
  }}
  .gear-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
  }}
  .gear {{
    min-height: 112px;
    padding: 12px 10px;
    border-radius: 16px;
    background: var(--paper);
    border: 1px solid var(--line);
    box-shadow: 0 8px 18px rgba(84,55,18,.06);
  }}
  .gear-mark {{
    width: 34px;
    height: 34px;
    display: grid;
    place-items: center;
    margin-bottom: 10px;
    border-radius: 11px;
    color: #fff;
    font-size: 15px;
    font-weight: 950;
    background: var(--green);
  }}
  .gear:nth-child(2) .gear-mark {{ background: var(--water); }}
  .gear:nth-child(3) .gear-mark {{ background: var(--orange); }}
  .gear:nth-child(4) .gear-mark {{ background: var(--red); }}
  .gear:nth-child(5) .gear-mark {{ background: #697d45; }}
  .gear:nth-child(6) .gear-mark {{ background: #8a63b8; }}
  .gear:nth-child(7) .gear-mark {{ background: #bf7f36; }}
  .gear:nth-child(8) .gear-mark {{ background: #4f789d; }}
  .gear strong {{
    display: block;
    font-size: 16px;
    font-weight: 950;
  }}
  .gear > span:not(.gear-mark) {{
    display: block;
    margin-top: 5px;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.35;
    font-weight: 650;
  }}
  .callout {{
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 15px;
    background: linear-gradient(90deg, var(--mint), #fff);
    border: 1px solid rgba(0,128,66,.2);
    color: var(--green-dark);
    font-size: 14px;
    line-height: 1.55;
    font-weight: 800;
  }}
  .bait-layout {{
    display: grid;
    grid-template-columns: .92fr 1.08fr;
    gap: 14px;
  }}
  .bait-focus {{
    padding: 18px;
    border-radius: 20px;
    background:
      linear-gradient(145deg, rgba(255,197,32,.92), rgba(255,138,0,.9));
    color: #5a2c00;
    box-shadow: 0 14px 24px rgba(188,102,0,.18);
  }}
  .bait-focus .big {{
    display: block;
    margin-bottom: 8px;
    font-size: 38px;
    line-height: 1.02;
    font-weight: 950;
  }}
  .bait-focus p {{
    margin: 0;
    color: #653908;
    font-size: 15px;
    line-height: 1.55;
    font-weight: 800;
  }}
  .steps {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }}
  .mini-step {{
    padding: 13px;
    border-radius: 16px;
    background: #fff;
    border: 1px solid var(--line);
  }}
  .mini-step b {{
    display: inline-flex;
    width: 24px;
    height: 24px;
    align-items: center;
    justify-content: center;
    margin-right: 6px;
    border-radius: 8px;
    background: var(--green);
    color: #fff;
    font-size: 12px;
    font-weight: 950;
  }}
  .mini-step strong {{
    font-size: 16px;
    font-weight: 950;
  }}
  .mini-step span {{
    display: block;
    margin-top: 8px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.45;
    font-weight: 650;
  }}
  .position-grid {{
    display: grid;
    grid-template-columns: 1.2fr .8fr;
    gap: 14px;
  }}
  .rank-list {{
    display: grid;
    gap: 10px;
  }}
  .rank {{
    display: grid;
    grid-template-columns: 48px 1fr;
    gap: 12px;
    align-items: center;
    padding: 14px;
    border-radius: 18px;
    background: #fff;
    border: 1px solid var(--line);
  }}
  .rank-badge {{
    display: grid;
    place-items: center;
    width: 48px;
    height: 48px;
    border-radius: 16px;
    background: var(--green);
    color: #fff;
    font-size: 18px;
    font-weight: 950;
  }}
  .rank:nth-child(2) .rank-badge {{ background: var(--water); }}
  .rank:nth-child(3) .rank-badge {{ background: var(--orange); }}
  .rank strong {{
    display: block;
    font-size: 18px;
    font-weight: 950;
  }}
  .rank > div span {{
    display: block;
    margin-top: 5px;
    color: var(--muted);
    font-size: 13px;
    line-height: 1.45;
    font-weight: 650;
  }}
  .watch-box {{
    padding: 18px;
    border-radius: 20px;
    background: var(--water-soft);
    border: 2px solid rgba(45,169,233,.3);
  }}
  .watch-box h3 {{
    margin: 0 0 10px;
    color: #0d6f9e;
    font-size: 20px;
    line-height: 1.2;
    font-weight: 950;
  }}
  .watch-box p {{
    margin: 0 0 10px;
    color: #28556a;
    font-size: 14px;
    line-height: 1.55;
    font-weight: 750;
  }}
  .no-go {{
    margin-top: 10px;
    padding: 10px 12px;
    border-radius: 13px;
    background: #fff3f1;
    color: var(--red);
    font-size: 13px;
    line-height: 1.5;
    font-weight: 850;
  }}
  .signal {{
    overflow: hidden;
    border-radius: 20px;
    border: 2px solid var(--green);
    background: #fff;
    box-shadow: 0 10px 22px rgba(0,128,66,.1);
  }}
  .signal-row {{
    display: grid;
    grid-template-columns: 120px 1fr 142px;
    min-height: 76px;
    border-bottom: 1px solid var(--line);
  }}
  .signal-row:last-child {{ border-bottom: 0; }}
  .phase {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 12px 14px;
    color: #fff;
    font-weight: 950;
  }}
  .signal-row:nth-child(1) .phase {{ background: #6d9a69; }}
  .signal-row:nth-child(2) .phase {{ background: var(--orange); }}
  .signal-row:nth-child(3) .phase {{ background: var(--red); }}
  .phase small {{
    display: block;
    margin-top: 3px;
    opacity: .84;
    font-size: 11px;
    font-weight: 850;
  }}
  .signal-text {{
    padding: 15px 16px;
    font-size: 16px;
    line-height: 1.5;
    font-weight: 800;
  }}
  .signal-action {{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px;
    text-align: center;
    font-size: 16px;
    line-height: 1.3;
    font-weight: 950;
    background: #fff8e9;
  }}
  .memory-banner {{
    margin-top: 16px;
    padding: 18px 14px;
    border-radius: 20px;
    text-align: center;
    color: #fff;
    background: linear-gradient(90deg, var(--red), var(--orange), var(--gold));
    box-shadow: 0 14px 24px rgba(228,56,40,.18);
  }}
  .memory-banner span {{
    display: block;
    font-size: 32px;
    line-height: 1.15;
    font-weight: 950;
  }}
  .memory-banner small {{
    display: block;
    margin-top: 6px;
    font-size: 13px;
    font-weight: 850;
    color: rgba(255,255,255,.92);
  }}
  .lift-time {{
    display: grid;
    grid-template-columns: .95fr 1.05fr;
    gap: 14px;
  }}
  .lift-card, .time-card {{
    padding: 18px;
    border-radius: 20px;
    background: #fff;
    border: 1px solid var(--line);
  }}
  .lift-card h3, .time-card h3 {{
    margin: 0 0 14px;
    font-size: 20px;
    font-weight: 950;
  }}
  .lift-list {{
    display: grid;
    gap: 10px;
  }}
  .lift-item {{
    display: grid;
    grid-template-columns: 34px 1fr;
    gap: 10px;
    align-items: center;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.45;
    font-weight: 750;
  }}
  .lift-item b {{
    display: grid;
    place-items: center;
    width: 34px;
    height: 34px;
    border-radius: 12px;
    background: var(--green);
    color: #fff;
  }}
  .time-row {{
    display: grid;
    grid-template-columns: 76px 1fr;
    gap: 10px;
    align-items: center;
    margin-bottom: 9px;
    font-size: 13px;
    font-weight: 850;
    color: var(--muted);
  }}
  .bar {{
    height: 18px;
    border-radius: 999px;
    background: #eee2cd;
    overflow: hidden;
  }}
  .bar i {{
    display: block;
    height: 100%;
    border-radius: inherit;
    background: var(--green);
  }}
  .bar.gold i {{ background: linear-gradient(90deg, var(--gold), var(--orange)); }}
  .bar.bad i {{ background: #99bd91; }}
  .time-note {{
    margin-top: 12px;
    padding: 10px;
    border-radius: 13px;
    background: var(--mint);
    color: var(--green-dark);
    font-size: 13px;
    line-height: 1.45;
    font-weight: 850;
  }}
  .mnemonic {{
    padding: 24px;
    border-radius: 24px;
    background: linear-gradient(180deg, #fff, #fffaf0);
    border: 2px solid var(--green);
    box-shadow: 0 14px 28px rgba(0,128,66,.08);
  }}
  .mnemonic-title {{
    text-align: center;
    margin-bottom: 18px;
  }}
  .mnemonic-title strong {{
    display: block;
    color: var(--green);
    font-size: 30px;
    line-height: 1.2;
    font-weight: 950;
  }}
  .mnemonic-title span {{
    display: block;
    margin-top: 6px;
    color: var(--muted);
    font-size: 14px;
    font-weight: 750;
  }}
  .mnemonic-grid {{
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
  }}
  .mnemonic-item {{
    min-height: 102px;
    padding: 10px 6px;
    border-radius: 15px;
    background: var(--rice);
    text-align: center;
    border: 1px solid var(--line);
  }}
  .mnemonic-item b {{
    display: block;
    color: var(--green);
    font-size: 30px;
    line-height: 1;
    font-weight: 950;
  }}
  .mnemonic-item span {{
    display: block;
    margin-top: 8px;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.35;
    font-weight: 750;
  }}
  .safety {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }}
  .safe-box {{
    padding: 16px;
    border-radius: 18px;
    background: var(--mint);
    border: 1px solid rgba(0,128,66,.26);
  }}
  .safe-box.danger {{
    background: #fff2f0;
    border-color: rgba(228,56,40,.3);
  }}
  .safe-box h3 {{
    margin: 0 0 10px;
    color: var(--green);
    font-size: 19px;
    font-weight: 950;
  }}
  .safe-box.danger h3 {{ color: var(--red); }}
  .safe-box p {{
    margin: 0 0 7px;
    color: var(--ink);
    font-size: 14px;
    line-height: 1.45;
    font-weight: 750;
  }}
  .footer {{
    margin-top: 28px;
    padding: 28px 26px 30px;
    background: var(--green);
    color: #fff;
    text-align: center;
  }}
  .footer strong {{
    display: block;
    font-size: 25px;
    line-height: 1.25;
    font-weight: 950;
  }}
  .footer span {{
    display: block;
    margin-top: 8px;
    color: rgba(255,255,255,.78);
    font-size: 13px;
    line-height: 1.5;
    font-weight: 750;
  }}
  .poster:not(.topic-full) .topic-section {{ display: none; }}
  .poster.topic-equipment .topic-equipment-section,
  .poster.topic-bait .topic-bait-section,
  .poster.topic-position .topic-position-section,
  .poster.topic-signal .topic-signal-section,
  .poster.topic-lift .topic-lift-section,
  .poster.topic-time .topic-time-section,
  .poster.topic-mnemonic .topic-mnemonic-section,
  .poster.topic-safety .topic-safety-section {{ display: block; }}
  .poster.topic-lift .time-card,
  .poster.topic-time .lift-card {{ display: none; }}
  .poster.topic-lift .lift-time,
  .poster.topic-time .lift-time {{ grid-template-columns: 1fr; }}
  .poster:not(.topic-full) .footer {{ margin-top: 34px; }}
</style>
</head>
<body>
<main class="poster topic-{topic}">
  <section class="hero">
    <div class="brand-row">
      <img src="data:image/png;base64,{farm_logo}" alt="老乡农场">
      <span class="brand-divider"></span>
      <img class="wb-logo" src="data:image/png;base64,{wb_logo}" alt="WorkBuddy">
    </div>
    <div class="hero-grid">
      <div>
        <span class="eyebrow">老乡农场限定 · 鸡肠子钓小龙虾</span>
        <h1>{topic_data["title"]}</h1>
        <p class="subtitle">{topic_data["subtitle"]}</p>
        <div class="hero-points">
{hero_points}
        </div>
      </div>
      <div class="canal-card" aria-label="农场沟渠钓虾示意">
        <div class="sun-label">15:00-17:00 黄金档</div>
        <div class="grass"><i class="blade"></i><i class="blade"></i><i class="blade"></i><i class="blade"></i><i class="blade"></i></div>
        <div class="water"></div>
        <div class="line-stick"></div>
        <div class="fishing-line"></div>
        <div class="bait-dot">鸡肠子</div>
        <div class="cray"></div>
        <div class="dimension"><span>沟宽 1.6 米</span><span>水深 50cm</span></div>
      </div>
    </div>
  </section>

  <section class="section topic-section topic-equipment-section">
    <div class="section-head"><span class="num">1</span><h2>装备别复杂，轻巧最好用</h2><span class="section-kicker">窄沟适配</span></div>
    <div class="gear-grid">
      <div class="gear"><span class="gear-mark">竿</span><strong>1-1.5米竿</strong><span>短竿更稳，适合窄沟</span></div>
      <div class="gear"><span class="gear-mark">线</span><strong>1.2-1.8米线</strong><span>别太长，避免抛过沟</span></div>
      <div class="gear"><span class="gear-mark">钩</span><strong>6-8号虾钩</strong><span>钩尖微露，方便挂牢</span></div>
      <div class="gear"><span class="gear-mark">饵</span><strong>鸡肠子</strong><span>新鲜腥味，是核心诱因</span></div>
      <div class="gear"><span class="gear-mark">桶</span><strong>带盖水桶</strong><span>浅水暂养，防止逃跑</span></div>
      <div class="gear"><span class="gear-mark">网</span><strong>20-30cm抄网</strong><span>出水瞬间从下方接</span></div>
      <div class="gear"><span class="gear-mark">凳</span><strong>折叠凳</strong><span>等口更稳，动作更轻</span></div>
      <div class="gear"><span class="gear-mark">剪</span><strong>小剪刀</strong><span>现场剪饵，保持新鲜</span></div>
    </div>
    <div class="callout">窄沟技巧：线短一点、动作轻一点，落点宁可近草边，也别大力甩到水中央。</div>
  </section>

  <section class="section topic-section topic-bait-section">
    <div class="section-head"><span class="num">2</span><h2>鸡肠子饵料，气味要新鲜</h2><span class="section-kicker">诱虾关键</span></div>
    <div class="bait-layout">
      <div class="bait-focus"><span class="big">现穿<br>现用</span><p>清水冲掉杂质，但要保留腥味。3-5cm 一段，钩尖露 1-2mm，20 分钟没口就换。</p></div>
      <div class="steps">
        <div class="mini-step"><strong><b>1</b>清洗</strong><span>冲 2-3 遍，去杂质，留腥味。</span></div>
        <div class="mini-step"><strong><b>2</b>切割</strong><span>剪成 3-5cm 小段，别太碎。</span></div>
        <div class="mini-step"><strong><b>3</b>穿钩</strong><span>沿肠壁穿入，钩尖微露。</span></div>
        <div class="mini-step"><strong><b>4</b>加香</strong><span>滴 1-2 滴香油，气味扩散更远。</span></div>
      </div>
    </div>
  </section>

  <section class="section topic-section topic-position-section">
    <div class="section-head"><span class="num">3</span><h2>钓位按这个顺序找</h2><span class="section-kicker">先找藏身处</span></div>
    <div class="position-grid">
      <div class="rank-list">
        <div class="rank"><span class="rank-badge">1</span><div><strong>水草边缘</strong><span>草根内侧 10-20cm 是黄金落点，虾常在这里觅食。</span></div></div>
        <div class="rank"><span class="rank-badge">2</span><div><strong>沟渠拐角</strong><span>水流变缓，食物沉积，内弯位置更容易聚虾。</span></div></div>
        <div class="rank"><span class="rank-badge">3</span><div><strong>阴凉暗处 / 进水口</strong><span>石块、树根、进水口附近，藏身和溶氧条件更好。</span></div></div>
      </div>
      <div class="watch-box">
        <h3>看水面，判断有没有虾</h3>
        <p>小气泡持续冒出：底下可能有虾。</p>
        <p>水草轻轻抖动：虾可能正在觅食。</p>
        <p>岸边有爪印：这里常有虾活动。</p>
        <div class="no-go">避开：水流急、硬光秃底、正午暴晒、来回踩踏的岸边。</div>
      </div>
    </div>
  </section>

  <section class="section topic-section topic-signal-section">
    <div class="section-head"><span class="num">4</span><h2>咬钩信号，别提早</h2><span class="section-kicker">最容易空钩</span></div>
    <div class="signal">
      <div class="signal-row"><div class="phase">探测期<small>线微抖</small></div><div class="signal-text">竿尖轻颤、线有小动作，虾还在试探。</div><div class="signal-action">完全不动</div></div>
      <div class="signal-row"><div class="phase">夹持期<small>线走慢</small></div><div class="signal-text">线被缓慢拉紧、持续下坠，虾夹住饵在拖。</div><div class="signal-action">再等 1-2 秒</div></div>
      <div class="signal-row"><div class="phase">吞食期<small>线快跑</small></div><div class="signal-text">线突然被快速拖入水中，手感明显变重。</div><div class="signal-action">立即提竿</div></div>
    </div>
    <div class="memory-banner"><span>抖不动，走再等，跑就提</span><small>这句记住，空钩会少一半</small></div>
  </section>

  <section class="section topic-section topic-lift-section topic-time-section">
    <div class="section-head"><span class="num">5</span><h2>提竿与时间，稳比猛重要</h2><span class="section-kicker">收获感来自节奏</span></div>
    <div class="lift-time">
      <div class="lift-card">
        <h3>提竿四步</h3>
        <div class="lift-list">
          <div class="lift-item"><b>1</b><span>确认线在“跑”，不是轻轻抖。</span></div>
          <div class="lift-item"><b>2</b><span>手腕上扬 30-45°，像抖掉水珠。</span></div>
          <div class="lift-item"><b>3</b><span>感觉有重量后，匀速收线。</span></div>
          <div class="lift-item"><b>4</b><span>快出水时，抄网从下方接住。</span></div>
        </div>
      </div>
      <div class="time-card">
        <h3>最佳垂钓时间</h3>
        <div class="time-row"><span>5:00-7:00</span><div class="bar gold"><i style="width:100%"></i></div></div>
        <div class="time-row"><span>7:00-9:00</span><div class="bar"><i style="width:82%"></i></div></div>
        <div class="time-row"><span>11:00-15:00</span><div class="bar bad"><i style="width:35%"></i></div></div>
        <div class="time-row"><span>15:00-17:00</span><div class="bar gold"><i style="width:100%"></i></div></div>
        <div class="time-row"><span>17:00-19:00</span><div class="bar"><i style="width:86%"></i></div></div>
        <div class="time-note">农场推荐：15:00-17:00。光线好、温度适宜，也更方便观察线和水草。</div>
      </div>
    </div>
  </section>

  <section class="section topic-section topic-mnemonic-section">
    <div class="mnemonic">
      <div class="mnemonic-title"><strong>钓虾七字诀</strong><span>把动作拆成 7 个字，新手也能快速上手</span></div>
      <div class="mnemonic-grid">
        <div class="mnemonic-item"><b>站</b><span>站草边<br>轻手轻脚</span></div>
        <div class="mnemonic-item"><b>抛</b><span>抛草边<br>宁近勿远</span></div>
        <div class="mnemonic-item"><b>等</b><span>线抖别急<br>线跑再提</span></div>
        <div class="mnemonic-item"><b>提</b><span>手腕上扬<br>巧劲发力</span></div>
        <div class="mnemonic-item"><b>抄</b><span>露水即接<br>别手抓</span></div>
        <div class="mnemonic-item"><b>摘</b><span>捏背中段<br>避开大钳</span></div>
        <div class="mnemonic-item"><b>养</b><span>浅水入桶<br>盖紧防逃</span></div>
      </div>
      <div class="callout">鸡肠子口诀：洗两遍，剪三段，钩尖微露最划算；现穿现用效果赞，二十分钟换一轮。</div>
    </div>
  </section>

  <section class="section topic-section topic-safety-section">
    <div class="section-head"><span class="num">6</span><h2>安全提醒，玩得开心也要稳</h2><span class="section-kicker">亲子活动必看</span></div>
    <div class="safety">
      <div class="safe-box">
        <h3>这样做</h3>
        <p>穿防滑鞋，不站陡坡边缘。</p>
        <p>小朋友必须有大人陪同。</p>
        <p>垃圾全部带走，桶里加浅水。</p>
        <p>被夹了放水里，别甩手。</p>
      </div>
      <div class="safe-box danger">
        <h3>不要这样</h3>
        <p>不要雷雨天、暴雨天垂钓。</p>
        <p>不要直接手抓虾的大钳。</p>
        <p>不要使用化学诱饵。</p>
        <p>不要破坏水草和沟渠环境。</p>
      </div>
    </div>
  </section>

  <footer class="footer">
    <strong>老乡农场钓虾指南</strong>
    <span>WorkBuddy AI 生成 · 老乡农场专用<br>鸡肠子配小龙虾，今天稳稳上岸</span>
  </footer>
</main>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Build WorkBuddy fishing guide HTML")
    parser.add_argument(
        "--topic",
        default="full",
        choices=sorted(TOPICS.keys()),
        help="生成主题：full/equipment/bait/position/signal/lift/time/mnemonic/safety",
    )
    parser.add_argument("--output", default=OUT, help="输出 HTML 路径")
    args = parser.parse_args()

    html = build_html(args.topic)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
