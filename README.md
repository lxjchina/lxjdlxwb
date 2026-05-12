# 老乡鸡钓龙虾技巧 Skill

专为**老乡鸡农场环境**定制的钓小龙虾技巧 Skill，适配宽 1.6 米、深 50cm 的沟渠环境，使用鸡肠子作为饵料。

## 功能特性

- **完整钓虾知识体系**：8 大模块覆盖装备、饵料、钓位、信号识别、提竿技巧、时间选择、进阶技巧、安全规范
- **图文教学生成**：一键生成精美 HTML 教学长图，适配手机端预览
- **PNG 导出**：通过 Chrome Headless 将 HTML 转为高清 PNG 图片
- **老乡鸡品牌规范**：严格遵循老乡鸡品牌色（#008042）、思源黑体排版
- **触发词丰富**：支持「钓龙虾技巧」「钓龙虾」「钓龙虾教学」「老乡农场钓龙虾」等多种说法
- **Logo 品牌展示**：Header 居中展示老乡农场 + 鸡窝小助手双 Logo，竖线分隔

## 文件结构

```
lxjdlxwb/
├── SKILL.md                 # Skill 定义文件（触发词、使用说明）
├── README.md                # 本文件
├── WK.png                  # 鸡窝小助手 logo（白字）
├── 老乡农场 logo.png         # 老乡农场 logo
├── scripts/
│   ├── generate-fishing-guide.html   # 教学长图 HTML 模板（主文件·推荐）
│   ├── generate-guide-v3.py        # PNG 生成脚本（Pillow 版）
│   ├── generate-reliable.py         # 一键生成脚本（含验证）
│   ├── html-to-png.py              # Chrome Headless 截图脚本
│   └── generate-topic-html.py      # 按主题生成 HTML 的工具脚本
└── references/
    └── 老乡鸡设计规范.md
```

## 安装

将整个 `lxjdlxwb/` 文件夹放入 WorkBuddy 的 skills 目录：

```bash
# 方式一：复制到用户 skills 目录（所有项目可用）
cp -r lxjdlxwb/ ~/.workbuddy/skills/

# 方式二：复制到项目 skills 目录（仅当前项目可用）
cp -r lxjdlxwb/ <项目路径>/.workbuddy/skills/
```

## 使用方式

### 触发 Skill

对 AI 说以下任意一句话即可触发：

- `钓龙虾技巧`
- `钓龙虾`
- `钓龙虾教学`
- `老乡农场钓龙虾`
- `鸡肠子钓虾`
- `生成钓虾图`

### 生成教学长图（HTML）

Skill 会调用 `scripts/generate-fishing-guide.html`，直接在浏览器中打开即可预览，无需任何构建步骤。

```bash
# macOS 直接预览
open scripts/generate-fishing-guide.html
```

### 导出 PNG 图片

**方式一：使用 Pillow（Python）**
```bash
cd lxjdlxwb/scripts
python3 generate-reliable.py
# 输出：scripts/output/diaoxiapu_guide_v3.png
```

**方式二：使用 Chrome Headless（推荐，效果更好）**
```bash
cd lxjdlxwb/scripts
python3 html-to-png.py
```

## HTML 模板说明

`generate-fishing-guide.html` 是主文件，特点：

- **零依赖**：单文件，内联 CSS，无外部依赖
- **响应式**：680px 宽度，手机端预览效果最佳
- **品牌规范**：严格遵循老乡鸡品牌色（#008042）
- **Logo 居中**：Header 老乡农场 logo + 鸡窝小助手 logo 并排居中，竖线分隔
- **字号放大**：正文 15px、章节标题 24px、七字诀 30px，手机阅读清晰
- **Logo 反白**：绿色 Header 背景上 logo 自动反白显示

> 注意：HTML 模板中的 logo 路径为 `../WK.png` 和 `../老乡农场 logo.png`，
> 请确保文件目录结构如上所示，或将 logo 放入 `scripts/` 目录并修改路径。

## 品牌规范

| 元素 | 规范 |
|------|------|
| 主色 | `#008042`（老乡鸡绿） |
| 辅色 | `#FFC520`（金）`#BFB08F`（米）`#E9DBCC`（浅米） |
| 强调色 | `#E43828`（红） |
| 字体 | Source Han Sans CN / PingFang SC / Microsoft YaHei |
| 图片宽度 | 680px（移动端优化） |

## 钓虾七字诀

> **站** → 选位站草边，轻手又轻脚
> **抛** → 饵抛草边落，宁近不要远
> **等** → 线抖不要急，线跑再出手
> **提** → 巧劲向上抖，匀速慢慢收
> **抄** → 虾露快下网，千万别手抓
> **摘** → 背后来下手，安全记心间
> **养** → 桶中加浅水，盖紧防逃跑

## 依赖

- Python 3.7+
- Pillow（`pip install Pillow`）
- Chrome / Chromium（html-to-png.py 需要）
- 中文字体：PingFang SC（macOS 自带）或思源黑体

## License

MIT
