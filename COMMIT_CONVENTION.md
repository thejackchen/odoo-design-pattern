# Commit Message 规范

采用 Odoo 社区风格前缀。

## 格式

```
[PREFIX] module_name: 简要描述（英文）
```

## 前缀

| 前缀 | 含义 | 示例 |
|------|------|------|
| `[ADD]` | 新增功能/模块 | `[ADD] myco_sale_approval: add sales approval workflow` |
| `[FIX]` | 修复缺陷 | `[FIX] myco_stock_wave: avoid N+1 in picking count` |
| `[IMP]` | 改进已有功能 | `[IMP] myco_base_core: extract approval mixin` |
| `[REF]` | 重构（不改变行为） | `[REF] myco_sale: split confirm into hook methods` |
| `[PERF]` | 性能优化 | `[PERF] myco_stock: batch write for wave assignment` |
| `[REM]` | 移除功能/代码 | `[REM] myco_sale: remove deprecated x_old_state field` |
| `[DEP]` | 标记废弃 | `[DEP] myco_base: deprecate legacy sync helper` |
| `[SEC]` | 安全修复 | `[SEC] myco_api: add rate limiting to webhook endpoint` |
| `[TEST]` | 仅测试变更 | `[TEST] myco_sale_approval: add multi-company test` |
| `[DOC]` | 仅文档变更 | `[DOC] myco_stock_wave: update README` |
| `[MIG]` | 数据迁移 | `[MIG] myco_sale: migrate approval_state values` |

## 规则

- 前缀后跟模块名，冒号分隔
- 描述用英文，祈使语气，首字母小写
- 单行不超过 72 字符
- 需要详细说明时空一行后写 body
