# Changelog

本文件记录 Odoo AI 开发工具包自身的变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循语义化版本。

## [2.1.0] - 2026-03-27

### Added
- `ARCHITECTURE_VISION.md`：架构愿景文档（大白话版），解释版本无关架构的思路和演进路径
- 对比 ERPNext / SAP / Salesforce 的设计模式，说明为什么要把业务知识从代码中分离
- 三步演进路线：方法拆小 → 规则外置 → 事件驱动

## [2.0.0] - 2026-03-27

### 全新重构

从 v1.x 的单文档规范重构为完整工具链。

### Added
- `Agent.md`：精简的 AI 开发指令（~200行），替代原 1000+ 行的单体规范
- `DEVELOPMENT_STANDARD.md`：完整开发规范（19章），作为 PR Review 审查依据
- `COMMIT_CONVENTION.md`：Odoo 风格 commit message 规范
- `.pre-commit-config.yaml`：ruff + pylint-odoo + 基础文件检查
- `.github/pull_request_template.md`：PR 提交模板
- `.github/workflows/pr-review.yml`：AI 自动审查 GitHub Action
- `.github/scripts/review_pr.py`：Claude API 审查脚本
- `_templates/module_template/`：完整的新模块脚手架
- `.claude/commands/odoo.md`：统一命令（setup / new / review）
- `install.sh`：一键安装脚本

### 架构变化
- 引入三层防线体系：Agent.md（开发时）→ Pre-commit（提交时）→ PR Review（合并前）
- 引入版本无关架构原则：业务规则层与 ORM 适配层分离
- 引入 slash commands 作为懒人包分发方式

### Removed
- `AI_Driven_Odoo_Development_Standard.md`（功能拆分到 Agent.md + DEVELOPMENT_STANDARD.md）
- `field_registry_template.csv`（字段治理规则融入规范，不再强制独立注册表）
- `module_catalog_template.csv`（模块治理规则融入规范）

## [1.1] - 2026-03-27

### Added
- 初版 `AI_Driven_Odoo_Development_Standard.md`（24 章完整规范）
- `field_registry_template.csv`
- `module_catalog_template.csv`
