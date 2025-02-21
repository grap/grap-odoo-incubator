# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    def quick_quantity_done(self):
        for move in self:
            initial_demand = move.product_uom_qty
            if initial_demand:
                move.quantity_done = initial_demand
                self._quantity_done_set()
            else:
                raise UserError(
                    _(
                        "We can't quickly set quantity done because there's no "
                        "initial demand or it's null."
                    )
                )
