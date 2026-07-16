# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """After Confirm, force stock.move to be full, ready to be validated"""
        res = super().action_confirm()
        self.mapped("picking_ids").quick_quantities_done()
        return res

    def action_quick_confirm_sale_and_picking(self):
        self.action_confirm()
        self.mapped("picking_ids").filtered(
            lambda x: x.state not in ["cancel", "done"]
        ).button_validate()
        return True

    def action_mass_quick_confirm_sale_and_picking(self):
        orders = self.browse(self.env.context.get("active_ids", []))
        action = self.env["confirmation.wizard"].confirm_message(
            _(
                "Are you sure you want to confirm the %(order_qty)s orders"
                " and the related deliveries ?",
                order_qty=len(orders),
            ),
            records=orders,
            title="Confirm",
            method="action_quick_confirm_sale_and_picking",
        )
        return action
