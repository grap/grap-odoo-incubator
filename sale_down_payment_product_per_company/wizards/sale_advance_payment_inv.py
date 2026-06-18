# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    product_message = fields.Char(compute="_compute_product_id", store=True)

    # Overwrite the function
    @api.depends("company_id", "sale_order_ids")
    def _compute_product_id(self):
        for wizard in self:
            company = wizard.mapped("sale_order_ids.company_id")
            if len(company) != 1:
                wizard.product_id = False
                wizard.product_message = _(
                    "Unable to select a down payment product for sale orders"
                    " related to many companies."
                    " Please create down payments selecting sale orders"
                    " of the single company."
                )
                continue

            amounts = wizard.mapped("sale_order_ids.order_line.tax_id.amount")
            if not amounts:
                products = company.down_payment_product_ids.filtered(
                    lambda x: len(x.taxes_id) == 0
                )
                if not products:
                    wizard.product_message = _(
                        "Unable to find a down payment product without taxes"
                        " for the company %(company_name)s."
                        " Please ask to your accountant"
                        " to configure down payments products.",
                        company_name=company.name,
                    )
            else:
                max_amount = max(amounts)
                products = company.down_payment_product_ids.filtered(
                    lambda x, max_amount=max_amount: x.mapped("taxes_id.amount")
                    == [max_amount]
                )
                if not products:
                    wizard.product_message = _(
                        "Unable to find a down payment product with taxes"
                        " %(max_amount)s for the company %(company_name)s."
                        " Please ask to your accountant"
                        " to configure down payments products.",
                        company_name=company.name,
                        max_amount=max_amount,
                    )
            if products:
                wizard.product_id = products[0]
                wizard.product_message = False
            else:
                wizard.product_id = False

    def _create_invoices(self, sale_orders):
        self.ensure_one()
        # Down payments situation
        if self.advance_payment_method != "delivered":
            if not self.product_id:
                raise UserError(_("Missing Down payment Product."))
        return super()._create_invoices(sale_orders)
