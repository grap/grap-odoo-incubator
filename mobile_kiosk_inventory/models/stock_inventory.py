# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    def mk_inventory_stock_inventory_select(self):
        self.ensure_one()
        return self.env["mobile.kiosk.inventory"]._hook_after_stock_inventory_selection(
            self
        )
