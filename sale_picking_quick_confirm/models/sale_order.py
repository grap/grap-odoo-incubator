# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_quick_confirm(self):
        """Quick Confirm Sale and All related Pickings"""
        super().action_confirm()
        for picking in self.mapped("picking_ids").filtered(
            lambda picking: picking.state not in ("cancel", "done")
        ):
            picking.quick_confirm()
        return True
