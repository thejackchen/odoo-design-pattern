#!/bin/bash
# Odoo 开发规范工具包 - 一键安装
# 安装 /odoo 命令到全局，之后在任何项目中都能用

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$HOME/.claude/commands"

mkdir -p "$TARGET_DIR"
cp "$REPO_DIR/.claude/commands/odoo.md" "$TARGET_DIR/odoo.md"

# 写入仓库路径到环境变量配置
SHELL_RC="$HOME/.zshrc"
[ -f "$SHELL_RC" ] || SHELL_RC="$HOME/.bashrc"

if ! grep -q "ODOO_DESIGN_PATTERN_HOME" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "export ODOO_DESIGN_PATTERN_HOME=\"$REPO_DIR\"" >> "$SHELL_RC"
fi

echo ""
echo "Done!"
echo ""
echo "已安装 /odoo 命令。"
echo "已设置 ODOO_DESIGN_PATTERN_HOME=$REPO_DIR"
echo ""
echo "使用方式（在 Claude Code 中）："
echo "  /odoo setup              初始化项目"
echo "  /odoo new myco_xxx       创建新模块"
echo "  /odoo review             审查代码"
echo "  /odoo                    自动检测"
echo ""
echo "请重新打开终端或运行: source $SHELL_RC"
