# -*- coding: utf-8 -*-
"""
Sample model template.
Rename this file and class to match your business object.
Follow the section ordering defined in Agent.md §3.1.
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SampleModel(models.Model):
    # ── 1. 元属性 ──
    _name = "module.sample"
    _description = "Sample Model"
    _order = "create_date desc"
    # _inherit = ["mail.thread", "mail.activity.mixin"]

    # ── 2. 字段：常规 → 关系 → 计算 ──
    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        # tracking=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    # ── 3. SQL 约束 ──
    # _sql_constraints = [
    #     ("name_company_uniq", "unique(name, company_id)", "Name must be unique per company."),
    # ]

    # ── 4. CRUD 覆写 ──
    # @api.model_create_multi
    # def create(self, vals_list):
    #     records = super().create(vals_list)
    #     return records

    # ── 5. compute ──

    # ── 6. onchange ──

    # ── 7. 约束 ──

    # ── 8. 业务动作 ──
    def action_confirm(self):
        self._check_can_confirm()
        self._do_confirm()

    def action_cancel(self):
        self.write({"state": "cancelled"})

    # ── 9. 私有业务方法 ──
    def _check_can_confirm(self):
        for record in self:
            if record.state != "draft":
                raise UserError(
                    _("Record '%s' is not in draft state.", record.name)
                )

    def _do_confirm(self):
        self.write({"state": "confirmed"})

    # ── 10. 定时任务 ──
