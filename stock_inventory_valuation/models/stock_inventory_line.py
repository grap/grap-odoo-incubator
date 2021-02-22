# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

import odoo.addons.decimal_precision as dp


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    # Columns section
    price_unit = fields.Float(
        string="Unit Price",
        compute="_compute_price_unit",
        store=True,
        digits=dp.get_precision("Product Price"),
        help="Technical field used to record the product cost at"
        " the time of the inventory",
    )

    valuation = fields.Float(
        string="Valuation",
        compute="_compute_valuation",
        store=True,
        digits=dp.get_precision("Product Price"),
    )

    # Compute Section
    @api.multi
    @api.depends("product_id")
    def _compute_price_unit(self):
        for line in self:
            line.price_unit = line.product_id and line.product_id.standard_price or 0.0

    @api.multi
    @api.depends("price_unit", "product_id", "product_qty")
    def _compute_valuation(self):
        for line in self:
            line.valuation = line.price_unit * line.product_qty
