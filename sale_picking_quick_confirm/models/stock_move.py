# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def quick_quantity_done(self):
        # Handling null quantities upstream in stock_picking quick_confirm()
        for move in self:
            move.quantity_done = move.product_uom_qty
            self._quantity_done_set()
