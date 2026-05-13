---
name: lxjdlxwb
description: >
  Use this skill whenever the user asks about 老乡农场/沟渠钓龙虾 or 钓小龙虾技巧, including 鸡肠子饵料、
  钓位、水草边、看线、咬钩信号、提竿、抄网、亲子安全、雷雨环保提醒, or asks to create/receive a 钓虾教学图、
  海报、长图, or image for WorkBuddy. It should answer ordinary questions with concise mobile-friendly text and,
  when the user explicitly wants an image, route to the bundled 1360px WorkBuddy PNG assets instead of generic AI image generation.
compatibility: "Requires Python 3 for helper scripts; prebuilt PNG delivery has no Chrome or Pillow dependency."
metadata:
  version: "2.4.1"
  tags: ["老乡鸡", "小龙虾", "农场", "钓虾", "鸡肠子", "WorkBuddy", "教学图"]
license: MIT
---

# 老乡鸡版钓小龙虾技巧 Skill

专为**老乡农场**环境定制：约 1.6 米宽、50cm 深的浅沟渠，使用鸡肠子作饵，面向 WorkBuddy 客户端和小程序稳定交付。

## 触发范围

用户提到以下意图时使用本 skill：

- 钓龙虾/钓小龙虾/钓虾技巧
- 老乡农场、沟渠、水草边、50cm 浅水
- 鸡肠子饵料、挂钩、诱虾
- 什么时候提竿、怎么看线、空钩、抄网
- 生成钓虾图、教学图、海报、长图

## 运行原则

1. **先文字，后图片**：普通技巧问题只回答文字；只有用户明确说“生成图片、发图、海报、长图、做一张”时才给图片。
2. **小程序短答优先**：默认 3-5 条短句，不用大表格，不输出长 Markdown，不暴露脚本过程。
3. **图片走确定性路径**：优先用 `assets/` 里的 1360px PNG；不要调用通用 AI 生图替代。
4. **失败不甩锅**：如果脚本不可用或 Chrome 不可用，直接使用内置兜底图；不要说“可能不符合要求”。
5. **安全优先**：涉及儿童、雷雨、夹手、沟渠边站位时，必须给安全提醒。

## 默认文字回复模板

普通技巧问题按这个结构回答，控制在小程序首屏可读范围内：

```text
可以，老乡农场这种 1.6 米浅沟，重点是轻、近、等。
1. 饵用鸡肠子，剪 3-5cm，钩尖微露。
2. 落点选水草边 10-20cm，不要甩太远。
3. 线微抖别动，线开始跑再提。
4. 出水前用抄网接，别直接手抓。

需要的话，我也可以给你发一张对应的钓虾教学图。
```

如果用户只问单点问题，回答更短。例如“什么时候提竿”：

```text
记住“抖不动，走再等，跑就提”。
线只是轻轻抖，先别提；线被慢慢拖走，再等 1-2 秒；线明显跑起来，就手腕轻提，再用抄网接。
```

## 图片交付流程

用户明确要图片时，先判断主题，再返回对应 PNG。WorkBuddy 小程序优先发送图片文件，不发送 HTML。

主题、关键词和路径的源文件是 `assets/guide-images.json`。脚本可用时始终让 `scripts/select-guide-image.py` 读取该 manifest；不要手写新关键词或复制一份新的主题映射。

| 主题 | 适用问题 | 图片 |
| --- | --- | --- |
| `full` | 完整技巧、总览、教学长图 | `assets/workbuddy-fishing-guide@2x.png` |
| `equipment` | 装备、钓竿、钓线、抄网 | `assets/workbuddy-fishing-guide-equipment@2x.png` |
| `bait` | 鸡肠子、饵料、挂钩、香油 | `assets/workbuddy-fishing-guide-bait@2x.png` |
| `position` | 钓位、哪里好钓、水草、沟渠 | `assets/workbuddy-fishing-guide-position@2x.png` |
| `signal` | 咬钩、看线、什么时候提、空钩 | `assets/workbuddy-fishing-guide-signal@2x.png` |
| `lift` | 提竿、收线、抄网、出水 | `assets/workbuddy-fishing-guide-lift@2x.png` |
| `time` | 几点、天气、下午、黄金档 | `assets/workbuddy-fishing-guide-time@2x.png` |
| `mnemonic` | 口诀、速记、新手步骤 | `assets/workbuddy-fishing-guide-mnemonic@2x.png` |
| `safety` | 安全、亲子、夹手、雷雨、环保 | `assets/workbuddy-fishing-guide-safety@2x.png` |

可执行脚本时用快速选择器：

```bash
python3 scripts/select-guide-image.py --text "鸡肠子怎么挂钩，生成图片" --json
```

脚本不可执行时，按上表直接选内置 PNG。回复用户时只说图片已准备好，并发送图片；不要展示命令、路径或调试日志。

## 本地更新图片

只有开发者需要更新版式、文案或素材时，才运行生成链路：

```bash
cd scripts
python3 generate-reliable.py --topic bait
```

交付前必须确认：

- `python3 scripts/check-workbuddy-ready.py` 通过。
- `validate-workbuddy-assets.py` 输出“全部通过”。
- PNG 宽度至少 1360px，顶部两个 logo 正常，内容不截断、不空白、不糊字。

## 知识与参考

- 需要判断图片主题、关键词或路径时读取 `assets/guide-images.json`。
- 需要完整钓虾知识时读取 `references/fishing-knowledge.md`。
- 需要 WorkBuddy 客户端/小程序交互约束时读取 `references/workbuddy-runtime.md`。
- 需要品牌颜色、字体、视觉气质时读取 `references/老乡鸡设计规范.md`。

核心口诀：**站、抛、等、提、抄、摘、养**。最关键一句：**抖不动，走再等，跑就提**。
