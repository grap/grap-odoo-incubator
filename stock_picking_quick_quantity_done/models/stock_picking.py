# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    show_quick_quantities_done = fields.Boolean(
        compute="_compute_show_quick_quantities_done",
        help="Technical field used to compute whether the quick quantities"
        " done button should be shown.",
    )

    @api.depends("move_ids.quantity_done", "move_ids.product_uom_qty")
    def _compute_show_quick_quantities_done(self):
        for picking in self:
            moves = picking.mapped("move_ids").filtered(
                lambda move: move.state not in ("draft", "cancel", "done")
            )
            picking.show_quick_quantities_done = any(
                moves.mapped("show_quick_quantity_done")
            )

    def quick_quantities_done(self):
        moves = self.mapped("move_ids").filtered(
            lambda move: move.state not in ("draft", "cancel", "done")
        )
        moves.quick_quantity_done()
