# Odoo AI 团队开发工具包

面向 AI 驱动的 Odoo 开发团队的规范、模板和自动化工具。

## 设计理念

**开发时轻约束，合并时严审查，将来能重构。**

```
开发阶段                    合并阶段                     将来
┌──────────┐              ┌────────────────┐           ┌──────────┐
│ Agent.md │  ── PR ──>   │ GitHub Action  │  ── ✓ ->  │ 统一架构  │
│ 轻量指令  │              │ AI 自动审查     │           │ 版本无关  │
│ 别挖坑    │              │ 对照完整规范    │           │ 可重构    │
└──────────┘              └────────────────┘           └──────────┘
```

## 安装

```bash
git clone <repo-url> ~/odoo-design-pattern
cd ~/odoo-design-pattern && ./install.sh
```

然后在任何 Odoo 项目里打开 Claude Code，输入：

```
/odoo setup              # 一键配置项目
/odoo new myco_xxx       # 创建新模块
/odoo review             # 审查代码
/odoo                    # 自动检测该做什么
```

同事安装也是同样两步。

## 项目结构

```
├── Agent.md                        # AI 开发指令（通用，不绑定特定 AI 工具）
├── DEVELOPMENT_STANDARD.md         # 完整开发规范（PR Review 审查依据）
├── COMMIT_CONVENTION.md            # Commit message 规范
├── CHANGELOG.md                    # 工具包变更记录
├── install.sh                      # 一键安装
├── .pre-commit-config.yaml         # 提交时自动检查
├── .claude/commands/
│   └── odoo.md                     # /odoo 命令（setup / new / review）
├── .github/
│   ├── pull_request_template.md    # PR 模板
│   ├── workflows/pr-review.yml    # AI 自动审查
│   └── scripts/review_pr.py       # 审查脚本
└── _templates/
    └── module_template/            # 新模块脚手架
```

## 三层防线

| 层 | 工具 | 时机 | 作用 |
|---|------|------|------|
| **Layer 1** | Agent.md | 写代码时 | AI 遵循基本规则，不挖坑 |
| **Layer 2** | Pre-commit | 提交时 | 自动拦截低级错误 |
| **Layer 3** | PR Review Action | 合并前 | AI 对照完整规范审查 |

## 不用 Claude Code？

Agent.md 是通用的 AI 指令文件，适用于任何 AI 开发工具。手动复制到项目即可：

```bash
cp Agent.md /path/to/your/odoo-project/       # 通用 AI 指令
cp .pre-commit-config.yaml /path/to/your/odoo-project/
cp -r .github /path/to/your/odoo-project/     # GitHub Action
cp -r _templates /path/to/your/odoo-project/  # 模块模板
```

## 升级

```bash
cd ~/odoo-design-pattern
git pull && ./install.sh
```

已配置的项目中再跑一次 `/odoo setup` 即可同步最新规范。

版本变更记录见 `CHANGELOG.md`。

## 许可

MIT License
