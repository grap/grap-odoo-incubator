# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def quick_confirm(self):
        for picking in self:
            moves = picking.mapped("move_ids").filtered(
                lambda move: move.state not in ("draft", "cancel", "done")
            )
            # Fill picking moves
            for move in moves:
                move.quick_quantity_done()
            # Validate picking
            picking.button_validate()
