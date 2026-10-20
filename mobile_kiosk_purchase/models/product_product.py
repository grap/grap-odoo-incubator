# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def mk_purchase_product_product_select(self):
        self.ensure_one()
        return self.env["mobile.kiosk.purchase"]._hook_after_product_product_selection(
            self, self.env.context.get("mk_purchase_supplier_id")
        )
