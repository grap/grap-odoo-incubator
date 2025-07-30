# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def quick_confirm(self):
        for picking in self:
            moves = picking.mapped("move_ids").filtered(
                lambda move: move.state not in ("draft", "cancel", "done")
            )
            # Handling null quantities
            moves_qty_zero = moves.filtered(lambda x: not x.product_uom_qty).mapped(
                "product_id.name"
            )
            moves_qty_zero_str = ", ".join(map(str, moves_qty_zero))
            if moves_qty_zero:
                raise UserError(
                    _(
                        "We can't quickly validate picking because there's "
                        "moves with a null demand: %s",
                        moves_qty_zero_str,
                    )
                )
            else:
                # Fill picking moves
                for move in moves:
                    move.quick_quantity_done()
                # Validate picking
                picking.button_validate()
