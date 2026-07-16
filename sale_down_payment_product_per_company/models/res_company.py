# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    down_payment_product_ids = fields.Many2many(
        string="Down Payment Products",
        comodel_name="product.product",
        check_company=True,
        help="Products used for payment advances in sale module."
        " Create a product per company and tax.",
        domain="[('type', '=', 'service')]",
    )
