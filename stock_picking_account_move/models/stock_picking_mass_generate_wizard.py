# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickingMassGenerateWizard(models.TransientModel):
    _name = "stock.picking.mass.generate.wizard"
    _description = "Wizard to mass generate account moves from stock pickings"

    # Default Section
    def _default_pickings_to_do(self):
        StockPicking = self.env["stock.picking"]
        selected_pickings = self.env.context.get("active_ids")
        pickings = StockPicking.search(
            [
                ("id", "in", selected_pickings),
                ("account_move_state", "=", "to_do"),
            ]
        )
        return pickings

    def _default_selected_use_qty(self):
        return len(self._default_pickings_to_do())

    # Columns Section
    pickings_to_do = fields.Many2many(
        comodel_name="stock.picking",
        string="Stock Pickings ready to generate Account Moves",
        readonly=True,
        default=_default_pickings_to_do,
    )

    pickings_to_do_qty = fields.Integer(
        string="Number of pickings for which an Account Move would be generated",
        readonly=True,
        default=_default_selected_use_qty,
    )

    # Action Section
    def apply_button(self):
        self.ensure_one()
        return self.pickings_to_do.generate_account_move()
