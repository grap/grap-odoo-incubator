# Copyright 2024 Sylvain LE GAL - GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrExpense(models.Model):
    _inherit = "hr.expense"

    tax_description = fields.Char(
        string="Tax Rate", compute="_compute_amount_tax", store=True
    )

    @api.depends("total_amount", "tax_ids", "currency_id")
    def _compute_amount_tax(self):
        res = super()._compute_amount_tax()
        for expense in self:
            expense.tax_description = " - ".join(
                [f"{tax.amount:.1f} %" for tax in expense.tax_ids]
            )
        return res
