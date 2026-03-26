#!/usr/bin/env python3
"""
PR AI Review Script
根据 DEVELOPMENT_STANDARD.md 中的评审清单自动审查 PR diff。
需要环境变量：ANTHROPIC_API_KEY, GH_TOKEN
"""

import json
import os
import subprocess
import sys
import urllib.request

PR_NUMBER = sys.argv[1]
API_KEY = os.environ["ANTHROPIC_API_KEY"]
REPO = os.environ.get("GITHUB_REPOSITORY", "")

# ── 读取审查规范 ──
STANDARD_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "DEVELOPMENT_STANDARD.md")
try:
    with open(STANDARD_FILE, encoding="utf-8") as f:
        standard = f.read()
except FileNotFoundError:
    standard = "（未找到 DEVELOPMENT_STANDARD.md，使用内置基础规则）"

# ── 读取 diff ──
with open("/tmp/pr_diff_trimmed.txt", encoding="utf-8") as f:
    diff = f.read()

if not diff.strip():
    print("No diff found, skipping review.")
    sys.exit(0)

# ── 构建 prompt ──
SYSTEM_PROMPT = """你是一个 Odoo 代码评审专家。你的任务是根据团队开发规范审查 PR diff。

审查规范：
{standard}

输出格式要求：
## 🚫 Blocker（必须修复才能合并）
- 列出问题，引用具体代码行

## ⚠️ Warning（建议修改）
- 列出问题，引用具体代码行

## ℹ️ Info（提示信息）
- 建议和提示

## ✅ 总结
- 一句话总结 PR 质量

规则：
- 重点检查第 17 节的 15 项清单
- 只关注 diff 中实际变更的代码，不要评审未变更的上下文
- 如果 diff 很小且没有问题，简短回复即可
- 用中文输出
""".format(standard=standard[:30000])  # 截断规范避免超限

USER_PROMPT = f"""请审查以下 PR diff：

```diff
{diff}
```"""

# ── 调用 Claude API ──
payload = json.dumps({
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 4096,
    "system": SYSTEM_PROMPT,
    "messages": [{"role": "user", "content": USER_PROMPT}],
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=payload,
    headers={
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    },
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    review_text = result["content"][0]["text"]
except Exception as e:
    print(f"API call failed: {e}")
    sys.exit(1)

# ── 发布评论到 PR ──
comment_body = f"## 🤖 AI Code Review\n\n{review_text}\n\n---\n*Powered by Claude | 审查依据：DEVELOPMENT_STANDARD.md*"

cmd = [
    "gh", "pr", "comment", PR_NUMBER,
    "--body", comment_body,
]

try:
    subprocess.run(cmd, check=True, env={**os.environ})
    print("Review posted successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to post comment: {e}")
    # 回退：输出到 stdout
    print(comment_body)
    sys.exit(1)
