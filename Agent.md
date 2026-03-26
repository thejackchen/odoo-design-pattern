# Odoo AI 开发指令

> 本文件用于指导 AI Agent 在 Odoo 项目中的开发行为。
> 适用于任何 AI 开发工具（Claude Code、Cursor、Copilot 等）。
> 放入项目根目录或 AI 工具的系统指令配置中。

## 基线

- Odoo 版本：18.0（如项目另有说明，以项目为准）
- Python：3.10+
- 所有定制通过 Odoo 标准扩展点完成

---

## 一、绝对禁止

以下规则没有例外。违反任何一条必须立即修正。

1. **不修改 Odoo 官方源码**——所有定制走继承、xpath、patch、数据文件
2. **不复制官方整份视图 XML**——只用 `xpath` 做外科手术式修改
3. **不硬编码数据库 ID**——用 `self.env.ref('module.xml_id')`
4. **不手动 `commit()` / `rollback()`**——除非你显式创建了独立 cursor 并完整处理异常
5. **不在 `compute` / `onchange` 中写业务副作用**——不创建记录、不发消息、不改其他模型
6. **不在未做复用检查的情况下新增字段**——必须先确认无同语义字段可复用
7. **不用 `sudo()` 包裹整个方法**——只对最小操作、最小 recordset 使用，并注释原因
8. **不在循环内执行 `search` / `search_count` / `_read_group`**——先批量查询，再分发到每条记录
9. **不猜测**——不确定字段名、方法签名、XML ID 是否存在时，先读源码确认
10. **不生成未读过目标文件的代码**——修改任何文件前必须先读取该文件当前内容

---

## 二、写代码前必须做

每次接到开发任务，按此顺序执行：

1. **读取目标文件**：要修改的 model、view、security 文件的当前内容
2. **确认真实性**：涉及的模型名、字段名、方法签名、XML ID 在当前代码中是否真实存在
3. **检查复用性**：如需新增字段或模型，先搜索项目中是否已有同语义对象
4. **确认依赖**：引用其他模块的对象时，确认 `__manifest__.py` 已声明依赖
5. **明确边界**：确认本次修改不会无意影响不相关的流程

---

## 三、代码结构

### 3.1 模型类内部排列顺序

```python
class MyModel(models.Model):
    # ── 1. 元属性 ──
    _name = 'my.model'
    _inherit = ['mail.thread']
    _description = 'My Model'
    _order = 'create_date desc'

    # ── 2. 字段：常规 → 关系 → 计算 ──
    name = fields.Char(required=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')])
    partner_id = fields.Many2one('res.partner')
    line_ids = fields.One2many('my.model.line', 'parent_id')
    total = fields.Float(compute='_compute_total', store=True)

    # ── 3. SQL 约束 ──
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique.'),
    ]

    # ── 4. CRUD 覆写 ──
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        return records

    def write(self, vals):
        return super().write(vals)

    # ── 5. compute / inverse / search ──
    @api.depends('line_ids.amount')
    def _compute_total(self): ...

    # ── 6. onchange ──
    @api.onchange('partner_id')
    def _onchange_partner_id(self): ...

    # ── 7. 约束 ──
    @api.constrains('name')
    def _check_name(self): ...

    # ── 8. 业务动作（公有方法，按钮触发）──
    def action_confirm(self): ...
    def action_cancel(self): ...

    # ── 9. 私有业务方法 ──
    def _prepare_confirmation_vals(self): ...
    def _check_can_confirm(self): ...

    # ── 10. 定时任务 ──
    def _cron_auto_close(self): ...
```

### 3.2 业务逻辑与 ORM 操作分离

这是版本无关架构的核心。业务判断提成独立方法，ORM 操作做薄包裹。

```python
# ✓ 好——业务规则独立，将来升级或重构只改薄层
def action_confirm(self):
    self._check_can_confirm()       # 业务校验
    self._do_confirm()              # ORM 操作
    self._post_confirm_actions()    # 后续联动

def _check_can_confirm(self):
    for record in self:
        if record._needs_approval() and not record.approved_by:
            raise UserError(_("Order %s requires approval.", record.name))

def _needs_approval(self):
    """纯业务规则，不依赖 ORM 细节，版本无关"""
    self.ensure_one()
    return self.amount_total > self.company_id.approval_threshold

# ✗ 坏——业务规则和 ORM 混在一起，改不动
def action_confirm(self):
    for order in self:
        if order.amount_total > 100000 and not order.approved_by:
            raise UserError("需要审批")
        order.write({'state': 'confirmed'})
        self.env['stock.picking'].create({...})
```

### 3.3 关键方法必须可被 override

复杂流程拆成小方法，让继承者可以精准覆写单个环节：

- `_prepare_*()` — 准备数据
- `_check_*()` / `_validate_*()` — 校验
- `_do_*()` — 执行核心操作
- `_post_*()` — 后续处理
- `_get_*()` — 获取可配置值（如阈值、策略）

### 3.4 Batch 思维

方法默认支持多条记录。单条方法开头写 `self.ensure_one()`。

```python
# ✓ 批量查询，一次完成
data = self.env['stock.picking']._read_group(
    [('sale_id', 'in', self.ids)], ['sale_id'], ['__count']
)
counts = {sale.id: count for sale, count in data}
for order in self:
    order.picking_count = counts.get(order.id, 0)

# ✗ N+1，每条记录一次查询
for order in self:
    order.picking_count = self.env['stock.picking'].search_count(
        [('sale_id', '=', order.id)]
    )
```

### 3.5 状态机设计

- Selection 值用有意义的英文词，不用数字
- 状态变更只通过 `action_*` 方法，禁止直接 `write({'state': ...})`
- 变更方法内部必须校验前置状态
- 转换矩阵集中定义

```python
_VALID_TRANSITIONS = {
    'draft': ['confirmed', 'cancelled'],
    'confirmed': ['done', 'cancelled'],
}

def _check_state_transition(self, new_state):
    for record in self:
        if new_state not in self._VALID_TRANSITIONS.get(record.state, []):
            raise UserError(_("Cannot move from %s to %s.", record.state, new_state))
```

---

## 四、命名规则

| 类型 | 规则 | 示例 |
|------|------|------|
| 模块名 | `{公司}_{业务域}_{能力}` | `myco_sale_approval` |
| Link 模块 | `{公司}_{域A}_{域B}_link` | `myco_sale_stock_link` |
| 模型 `_name` | `{域}.{对象}` 单数 | `sale.approval.policy` |
| Wizard | `{目标模型}.{动作}` | `sale.order.approve` |
| Mixin | `*.mixin` | `myco.approval.mixin` |
| Many2one 字段 | `*_id` | `policy_id` |
| One2many / M2m | `*_ids` | `line_ids` |
| Boolean 字段 | `is_` / `has_` / `can_` / `need_` | `is_approved` |
| 日期字段 | `*_date` / `*_datetime` | `approval_date` |
| 标准模型上的自定义字段 | 带业务前缀 | `approval_state`（不是 `state2`） |
| recordset 变量 | 不带 `_id` | `partner`（不是 `partner_id`） |
| 整数 ID 变量 | 带 `_id` | `partner_id = record.partner_id.id` |
| XML ID（视图） | `{model}_view_{type}` | `sale_order_view_form` |
| XML ID（动作） | `{model}_action` | `sale_order_action` |
| XML ID（安全组） | `{module}_group_{role}` | `myco_sale_group_approver` |

---

## 五、新增字段的强制检查

新增任何字段前，按顺序检查：

1. Odoo 标准模型中是否已有同语义字段？
2. 项目自定义模块中是否已有同语义字段？
3. 能否通过 `related` 字段解决？
4. 能否通过 compute 投影解决？
5. 是否仅 UI 展示需求，不需要持久化？

全部不满足时才允许新增。新增时必须声明：

- **Owner module**：谁创建、谁负责维护
- **读写权责**：谁写入、谁只读
- **字段类型**：canonical（权威）/ projection（投影）/ transitional（过渡）

---

## 六、安全最低要求

- 每个自定义模型必须有 `ir.model.access.csv`
- 敏感字段必须有 `groups=`（成本、毛利、审批意见等）
- 公有方法（不以 `_` 开头）视为可被 RPC 调用，必须内部校验状态和权限
- `sudo()` 使用前注释为什么必须绕过权限，使用后仍校验业务合法性
- 多公司相关模型必须设置 `company_id` + `check_company=True`

---

## 七、视图规则

- 只用 `xpath` 继承，不复制官方整份视图
- 锚点优先按字段 `name`、按钮 `name` 定位，避免脆弱的 DOM 层级定位
- 复杂显示条件沉淀为后端字段（如 `can_approve`），不在 XML 里写长表达式
- 按钮对应的后端方法必须再次校验状态和权限，不依赖前端可见性做安全控制

---

## 八、测试最低要求

以下改动必须附测试：

- 新模型或新流程
- 权限 / 安全变更
- 价格、库存、会计、审批逻辑
- 计算字段依赖变更
- 多公司逻辑
- 定时任务

每个测试至少覆盖：正常路径 + 批量路径 + 权限路径。

性能敏感逻辑建议补 `self.assertQueryCount()` 防止 N+1 退化。

---

## 九、Import 排列顺序

```python
# 1. 标准库
import logging
from datetime import datetime

# 2. 第三方库
import requests

# 3. Odoo 框架
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

# 4. 本模块
from .utils import some_helper
```

---

## 十、每次完成修改后必须输出

1. **改了什么**：修改的文件、模型、字段、视图清单
2. **为什么**：业务原因
3. **影响范围**：是否影响已有流程
4. **新增字段**：如有——owner、语义、为什么不能复用
5. **风险点**：sudo / raw SQL / 大批量 / 迁移需求 / 多公司影响
6. **测试**：覆盖了什么场景
