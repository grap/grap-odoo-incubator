# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    down_payment_product_ids = fields.Many2many(
        comodel_name="product.product",
        related="company_id.down_payment_product_ids",
        readonly=False,
    )
