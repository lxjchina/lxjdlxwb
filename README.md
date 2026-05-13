# 老乡鸡钓龙虾技巧 Skill

专为**老乡鸡农场环境**定制的钓小龙虾技巧 Skill，适配宽 1.6 米、深 50cm 的沟渠环境，使用鸡肠子作为饵料。

## 功能特性

- **完整钓虾知识体系**：8 大模块覆盖装备、饵料、钓位、信号识别、提竿技巧、时间选择、进阶技巧、安全规范
- **WorkBuddy 小程序适配**：HTML 自包含，图片资源 base64 内联，避免 logo 或元素丢失
- **高清图文生成**：一键生成 2x PNG 教学长图，适配手机端预览和转发
- **生成前后校验**：自动检查 HTML 资源、PNG 清晰度、非空白和完整性
- **触发词丰富**：支持「钓龙虾技巧」「钓龙虾」「钓龙虾教学」「老乡农场钓龙虾」等多种说法
## 文件结构

```
lxjdlxwb/
├── SKILL.md                 # Skill 定义文件（触发词、使用说明）
├── README.md                # 本文件
├── WK.png                  # 鸡窝小助手 logo（白字）
├── 老乡农场 logo.png         # 老乡农场 logo
├── scripts/
│   ├── generate-fishing-guide.html   # 当前生成的自包含 HTML（由脚本重建）
│   ├── build-workbuddy-guide.py      # 重建自包含 HTML 模板（内联 logo）
│   ├── generate-guide-v3.py        # PNG 生成脚本（Pillow 版）
│   ├── generate-reliable.py         # WorkBuddy 一键校验 + 高清生成脚本
│   ├── html-to-png.py              # Chrome Headless 2x 截图脚本
│   ├── validate-workbuddy-assets.py # HTML/PNG 完整性校验脚本
│   └── generate-topic-html.py      # 旧版分主题生成工具（保留作兼容）
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

### 默认交互：先文字，不主动生图

用户只问技巧时，默认先给简洁文字回答，不要一上来生成图片。适合配图的问题，可以在答案末尾引导：

```text
需要的话，我也可以给你生成一张对应主题的钓虾教学图。
```

用户明确说「生成图片」「做一张」「发图」「要图片」「生成教学图」后，再使用下面的图片生成命令。

### 生成 WorkBuddy 高清教学图

运行可靠生成脚本，会先按主题重建 HTML，再校验资源、导出 2x PNG，最后校验 PNG 是否清晰完整。

```bash
cd lxjdlxwb/scripts
python3 generate-reliable.py
# 输出：scripts/output/workbuddy-fishing-guide@2x.png
```

### 按用户问题生成主题图

```bash
# 用户问“鸡肠子怎么挂钩”
python3 generate-reliable.py --topic bait
# 输出：scripts/output/workbuddy-fishing-guide-bait@2x.png

# 用户问“在哪个位置好钓”
python3 generate-reliable.py --topic position

# 用户问“什么时候提竿”
python3 generate-reliable.py --topic signal
```

主题参数：

| 主题 | 参数 |
|------|------|
| 完整指南 | `full` |
| 装备准备 | `equipment` |
| 鸡肠子饵料 | `bait` |
| 钓位选择 | `position` |
| 咬钩信号 | `signal` |
| 提竿抄虾 | `lift` |
| 最佳时间 | `time` |
| 钓虾口诀 | `mnemonic` |
| 安全提醒 | `safety` |

### 预览 HTML

`scripts/generate-fishing-guide.html` 是自包含模板，可直接在浏览器中打开预览，无需构建步骤。

```bash
open scripts/generate-fishing-guide.html
```

如需重新生成模板中的内联 logo 和新版视觉样式：

```bash
python3 scripts/build-workbuddy-guide.py --topic bait
```

### 手动导出 PNG

```bash
python3 scripts/html-to-png.py scripts/generate-fishing-guide.html scripts/output/workbuddy-fishing-guide@2x.png --scale 2
python3 scripts/validate-workbuddy-assets.py scripts/generate-fishing-guide.html scripts/output/workbuddy-fishing-guide@2x.png
```

## HTML 模板说明

`generate-fishing-guide.html` 是主文件，特点：

- **零依赖**：单文件，内联 CSS，无外部依赖
- **小程序稳定**：logo 使用 `data:image/png;base64` 内联，不引用本地路径或网络图片
- **响应式**：680px 宽度，手机端预览效果最佳
- **品牌规范**：严格遵循老乡鸡品牌色（#008042）
- **Logo 居中**：Header 老乡农场 logo + 鸡窝小助手 logo 并排居中，竖线分隔
- **字号放大**：正文 15px、章节标题 24px、七字诀 30px，手机阅读清晰
- **高清导出**：默认 2x PNG，实际宽度约 1360px

> 注意：面向 WorkBuddy 小程序交付时，请使用 `scripts/output/workbuddy-fishing-guide@2x.png`。HTML 只作为预览源和截图源。

## WorkBuddy 验收标准

生成图发送前请确认：

- `validate-workbuddy-assets.py` 输出“全部通过”
- PNG 宽度不低于 1200px
- 顶部两个 logo 正常显示
- 装备、饵料、钓位、咬钩信号、提竿、时间、口诀、安全模块完整
- 没有截断、空白底、糊字、表格溢出

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

## 额外说明
不管做什么，先发个 skill 再说
这个版本我就不上抽奖了，求放过！
