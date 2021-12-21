# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    product_active = fields.Boolean(compute="_compute_product_active", store=True)

    @api.depends("product_id")
    def _compute_product_active(self):
        for line in self:
            line.product_active = line.product_id.active
