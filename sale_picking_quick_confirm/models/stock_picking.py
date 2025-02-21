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
            if not moves:
                raise UserError(_("Nothing to check the availability for."))
            # Fill picking
            for move in moves:
                move.quick_quantity_done()
            # Validate SO
            picking.button_validate()
