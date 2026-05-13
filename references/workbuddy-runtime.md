# WorkBuddy 客户端与小程序运行说明

## 响应模式

WorkBuddy 客户端可以承载较完整的 Markdown，但小程序更适合短文本和图片。默认按小程序最小能力设计：

- 普通问答：3-5 条短句，不超过一屏。
- 操作步骤：使用编号列表，不用复杂表格。
- 图片交付：发送 PNG 文件，不发送 HTML。
- 调试信息：不展示命令、路径、校验日志，除非用户明确问“产物在哪”。

## 小程序使用边界

小程序可以作为触发和展示入口，但不直接安装或执行 skill。正确链路是：

```text
小程序用户提问
→ WorkBuddy/Agent 环境触发 lxjdlxwb
→ Agent 选择短文字或内置 PNG
→ 小程序展示结果
```

不要在小程序端直接读取 `SKILL.md`、运行 `scripts/*.py`、启动 Chrome 截图，或渲染 `scripts/generate-fishing-guide.html`。这些逻辑属于 WorkBuddy/Agent 运行环境或本地开发更新流程。

## 意图判断

只问技巧时回答文字：

- “钓龙虾有什么技巧”
- “鸡肠子怎么挂”
- “什么时候提竿”
- “小朋友钓要注意什么”

明确要图时发送图片：

- “生成图片”
- “发我一张图”
- “做成教学长图”
- “来个海报”
- “把这个做成钓虾图”

## 图片路径策略

优先级：

1. 可执行脚本：运行 `python3 scripts/select-guide-image.py --text "<用户问题>" --json`，使用返回的 `path`。
2. 不可执行脚本：按 `SKILL.md` 主题表直接选择 `assets/` PNG。
3. 本地开发更新：使用 `scripts/generate-reliable.py` 重新生成到 `scripts/output/`。

线上不要默认运行 Chromium 截图链路，因为它慢且依赖环境。截图链路只用于开发者更新素材。

## 话术边界

推荐：

```text
可以，我给你发“鸡肠子饵料”这张教学图。
```

避免：

```text
我正在运行脚本生成图片。
图片可能不符合 WorkBuddy 要求。
你的环境可能没有 Chrome。
```

如果图片不可用，直接回到文字要点，并建议稍后使用完整指南图，不要编造已生成。

## 验收标准

内置图片必须满足：

- PNG 宽度至少 1360px。
- 文件能从 PNG 头读取尺寸。
- `assets/guide-images.json` 中每个主题都有真实文件。
- 每张图适合手机查看，顶部 logo、标题和主体模块不截断。

运行：

```bash
python3 scripts/check-workbuddy-ready.py
```
