# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    show_quick_quantities_done = fields.Boolean(
        compute="_compute_show_quick_quantities_done",
        help="Technical field used to compute whether the quick quantities"
        " done button should be shown.",
    )

    @api.depends("move_ids")
    def _compute_show_quick_quantities_done(self):
        for picking in self:
            moves = picking.mapped("move_ids").filtered(
                lambda move: move.state not in ("draft", "cancel", "done")
            )
            picking.show_quick_quantities_done = False
            for move in moves:
                picking.show_quick_quantities_done = (
                    True if move.show_quick_quantity_done else False
                )

    def quick_quantities_done(self):
        for picking in self:
            moves = picking.mapped("move_ids").filtered(
                lambda move: move.state not in ("draft", "cancel", "done")
            )
            if not moves:
                raise UserError(_("Nothing to check the availability for."))
            for move in moves:
                move.quick_quantity_done()
