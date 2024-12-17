# Copyright 2024 Sylvain LE GAL - GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    accounts = fields.Char(compute="_compute_accounting_settings")

    @api.depends(
        "company_id",
        "categ_id.property_account_income_categ_id",
        "categ_id.property_account_expense_categ_id",
        "property_account_income_id",
        "property_account_expense_id",
    )
    def _compute_accounting_settings(self):
        for template in self:
            company = template.company_id or self.env.company
            res = template.with_company(company)._get_product_accounts()
            expense_code = res["expense"] and res["expense"].code or "-"
            income_code = res["income"] and res["income"].code or "-"
            template.accounts = f"{expense_code} / {income_code}"
