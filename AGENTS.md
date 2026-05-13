# Repository Guidelines

## Project Structure & Module Organization

This repository contains the `lxjdlxwb` WorkBuddy skill for 老乡农场钓小龙虾 guidance and poster generation.

- `SKILL.md` defines trigger phrases, response rules, topics, and WorkBuddy delivery requirements.
- `README.md` documents installation, usage, topics, and visual acceptance criteria.
- `scripts/` contains Python utilities for building HTML, selecting images, exporting PNGs, and validating outputs.
- `assets/` stores prebuilt 2x fallback PNGs plus `guide-images.json`.
- `references/` stores brand and design references.

Generated output belongs in `scripts/output/`; do not treat it as source unless intentionally refreshing assets.

## Build, Test, and Development Commands

- `python3 scripts/select-guide-image.py --text "什么时候提竿"`: selects a prebuilt WorkBuddy PNG from `assets/`.
- `python3 scripts/select-guide-image.py --text "鸡肠子怎么挂钩" --json`: returns topic and image metadata.
- `python3 scripts/build-workbuddy-guide.py --topic bait`: rebuilds `scripts/generate-fishing-guide.html` for one topic.
- `cd scripts && python3 generate-reliable.py --topic bait`: rebuilds HTML, validates resources, exports a 2x PNG, then validates the PNG.
- `python3 scripts/validate-workbuddy-assets.py scripts/generate-fishing-guide.html`: checks that HTML assets are fully inline.
- `python3 scripts/validate-workbuddy-assets.py scripts/generate-fishing-guide.html scripts/output/workbuddy-fishing-guide-bait@2x.png`: validates both HTML and generated PNG.

PNG export requires Chrome or Chromium. PNG validation requires Pillow.

## Coding Style & Naming Conventions

Use Python 3 with 4-space indentation, standard-library modules where practical, and explicit UTF-8 handling for Chinese content. Keep scripts executable with a `#!/usr/bin/env python3` shebang and short module docstrings.

Name topic-specific files with the existing pattern: `workbuddy-fishing-guide-<topic>@2x.png`. Supported topics are `full`, `equipment`, `bait`, `position`, `signal`, `lift`, `time`, `mnemonic`, and `safety`.

## Testing Guidelines

There is no formal unit test suite. Treat validation scripts as required checks before changing generated HTML, image assets, or topic selection logic.

Before shipping image-related changes, confirm:

- HTML validation prints `全部通过`.
- Generated PNG width is at least `1360px`.
- Logos are base64-inline in HTML, not local paths or network URLs.
- Topic images are complete, nonblank, and not clipped.

## Commit & Pull Request Guidelines

Git history uses concise conventional-style prefixes such as `feat:` and `fix:`; keep that style, for example `fix: validate topic assets`.

Pull requests should include purpose, changed topics or scripts, validation commands, and generated asset paths. Include screenshots or PNG previews when visual output changes.

## Agent-Specific Instructions

For normal user questions, follow `SKILL.md`: answer with text first and only provide images after an explicit image request. Prefer the fast `assets/` selector for WorkBuddy delivery; use Chromium-based regeneration only when updating or debugging assets.
