# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        """After Confirm, force stock.move.line to be full, ready to be
        validated"""
        super().action_confirm()
        for picking in self.mapped("picking_ids").filtered(
            lambda picking: picking.state not in ("cancel", "done")
        ):
            picking.quick_quantities_done()
        return True
