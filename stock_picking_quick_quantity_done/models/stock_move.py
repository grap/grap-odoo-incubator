# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    show_quick_quantity_done = fields.Boolean(
        compute="_compute_show_quick_quantity_done",
        help="Technical field used to compute whether the quick quantity"
        " done button should be shown.",
    )

    def _compute_show_quick_quantity_done(self):
        for move in self:
            move.show_quick_quantity_done = bool(
                move.quantity_done < move.product_uom_qty
            )

    def quick_quantity_done(self):
        for move in self.filtered(lambda x: x.product_uom_qty):
            move.quantity_done = move.product_uom_qty
            self._quantity_done_set()
