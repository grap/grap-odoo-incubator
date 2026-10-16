# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    racking_ids = fields.Many2many(
        string="Rackings",
        comodel_name="stock.racking",
        domain=[("type", "=", "normal")],
    )
