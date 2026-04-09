# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (sylvain.legal@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    unit_valuation = fields.Float(
        digits="Product Price",
        compute="_compute_unit_valuation",
        store=True,
        readonly=False,
    )

    total_valuation = fields.Float(
        digits="Product Price",
        compute="_compute_total_valuation",
        store=True,
    )

    @api.depends("product_id", "product_uom")
    def _compute_unit_valuation(self):
        for move in self:
            if not move.product_id:
                move.unit_valuation = 0.0
                continue
            move = move.with_company(move.company_id)
            product_cost = move.product_id.standard_price

            if not product_cost:
                if not move.unit_valuation:
                    move.unit_valuation = 0.0
                    continue

            to_uom = move.product_uom
            from_uom = move.product_id.uom_id
            if to_uom and to_uom != from_uom:
                product_cost = from_uom._compute_price(
                    product_cost,
                    to_uom,
                )
            move.unit_valuation = product_cost

    @api.depends("product_id", "product_uom", "quantity_done", "unit_valuation")
    def _compute_total_valuation(self):
        for move in self:
            move.total_valuation = move.unit_valuation * move.quantity_done
