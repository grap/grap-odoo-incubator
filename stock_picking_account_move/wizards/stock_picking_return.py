# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    # Override
    def _create_returns(self):
        new_picking_id, pick_type_id = super()._create_returns()
        new_picking = self.env["stock.picking"].browse([new_picking_id])
        new_picking.is_return = True
        return new_picking_id, pick_type_id
