# 老乡鸡钓龙虾技巧 Skill

专为 **WorkBuddy 客户端和小程序**准备的老乡农场钓小龙虾 skill。它面向 1.6 米宽、50cm 深的浅沟渠场景，使用鸡肠子作饵，默认先给短文字建议，用户明确要图时再发送高清 PNG 教学图。

## 功能特性

- **客户端流畅问答**：普通技巧问题控制为 3-5 条短句，适合小程序首屏阅读。
- **确定性图片交付**：内置 9 张 1360px WorkBuddy 高清 PNG，避免通用 AI 生图导致糊字、缺 logo 或尺寸不稳。
- **快速选图**：`scripts/select-guide-image.py` 无 Chrome、无 Pillow 依赖，可按用户问题选择对应主题图。
- **本地生成链路**：需要更新素材时，可重建 HTML、导出 2x PNG 并校验。
- **渐进式上下文**：`SKILL.md` 只保留运行时决策，详细钓虾知识和 WorkBuddy 说明放在 `references/`。

## 文件结构

```text
lxjdlxwb/
├── SKILL.md                         # WorkBuddy 运行时指令
├── AGENTS.md                        # 仓库贡献指南
├── assets/
│   ├── guide-images.json            # 主题、关键词、图片路径 manifest
│   ├── workbuddy-fishing-guide@2x.png
│   └── workbuddy-fishing-guide-<topic>@2x.png
├── references/
│   ├── fishing-knowledge.md         # 钓虾知识库
│   ├── workbuddy-runtime.md         # 客户端/小程序交互约束
│   └── 老乡鸡设计规范.md
├── evals/
│   └── evals.json                   # skill-creator 评测提示集
└── scripts/
    ├── check-workbuddy-ready.py     # 轻量上线自检
    ├── select-guide-image.py        # 线上快速选图
    ├── generate-reliable.py         # 本地可靠生成链路
    ├── build-workbuddy-guide.py
    ├── html-to-png.py
    └── validate-workbuddy-assets.py
```

## 使用 `skills` 快速安装

本仓库根目录包含合法的 `SKILL.md`，可被 [`skills`](https://www.npmjs.com/package/skills) CLI 直接发现。

先查看仓库内可安装的 skill：

```bash
npx -y skills add lxjchina/lxjdlxwb --list
```

安装到 Codex 全局 skills 目录：

```bash
npx -y skills add lxjchina/lxjdlxwb --skill lxjdlxwb -a codex -g -y
```

安装到当前项目的 Codex skills 目录：

```bash
npx -y skills add lxjchina/lxjdlxwb --skill lxjdlxwb -a codex -y
```

本地开发时可验证当前工作区是否能被 `skills` 识别：

```bash
npm run skills:list
```

## 手动安装

将整个 `lxjdlxwb/` 文件夹放入 WorkBuddy skills 目录：

```bash
cp -r lxjdlxwb/ ~/.workbuddy/skills/
```

或复制到项目级 skills 目录：

```bash
cp -r lxjdlxwb/ <项目路径>/.workbuddy/skills/
```

## 使用方式

### 在小程序里怎么用

可以在 WorkBuddy 小程序对话里触发这个 skill，但小程序本身不是 skill 的安装或执行环境。请先在 WorkBuddy/Agent 运行环境安装并启用 `lxjdlxwb`，小程序用户再通过自然语言提问触发。

推荐链路：

```text
小程序用户提问
→ WorkBuddy/Agent 识别并触发 lxjdlxwb
→ 普通问题返回短文字
→ 明确要图时选择 assets/*.png
→ 小程序展示文本或图片
```

小程序端只负责发送问题和展示结果，不建议直接读取 `SKILL.md`、运行 Python 脚本、执行 Chrome 截图，或渲染 `scripts/generate-fishing-guide.html`。线上图片交付优先使用仓库内置 PNG。

触发示例：

- `钓龙虾技巧`
- `老乡农场钓龙虾`
- `鸡肠子怎么挂钩`
- `什么时候提竿`
- `生成钓虾教学图`

默认行为：

1. 用户只问技巧：回复简短文字，不主动生成图片。
2. 用户明确要图：选择 `assets/` 中对应的 2x PNG 并发送。
3. 开发者更新素材：再运行本地生成链路。

## 快速选图

```bash
python3 scripts/select-guide-image.py --text "鸡肠子怎么挂钩，生成图片"
# assets/workbuddy-fishing-guide-bait@2x.png

python3 scripts/select-guide-image.py --text "什么时候提竿" --json
```

主题参数：

| 主题 | 参数 |
| --- | --- |
| 完整指南 | `full` |
| 装备准备 | `equipment` |
| 鸡肠子饵料 | `bait` |
| 钓位选择 | `position` |
| 咬钩信号 | `signal` |
| 提竿抄虾 | `lift` |
| 最佳时间 | `time` |
| 钓虾口诀 | `mnemonic` |
| 安全提醒 | `safety` |

## 本地开发与校验

上线或提交前先跑轻量自检：

```bash
npm run check
```

验证当前工作区能被 `skills` CLI 识别：

```bash
npm run skills:list
```

重新生成某个主题图：

```bash
cd scripts
python3 generate-reliable.py --topic bait
```

手动校验 HTML 和 PNG：

```bash
python3 scripts/validate-workbuddy-assets.py scripts/generate-fishing-guide.html
python3 scripts/validate-workbuddy-assets.py scripts/generate-fishing-guide.html scripts/output/workbuddy-fishing-guide-bait@2x.png
```

## 交付标准

- `assets/guide-images.json` 中每个主题都有真实 PNG。
- PNG 宽度至少 1360px。
- 顶部两个 logo 正常显示。
- 内容不截断、不空白、不糊字。
- WorkBuddy 小程序交付图片文件，不直接发送 HTML。

## 依赖

- Python 3.7+
- `select-guide-image.py` 和 `check-workbuddy-ready.py` 无第三方依赖
- `generate-reliable.py` 需要 Chrome/Chromium
- PNG 深度校验需要 Pillow

## License

MIT
