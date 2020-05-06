# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MobileAppPurchase(models.TransientModel):
    _name = "mobile.app.purchase"
    _description = "Mobile App Purchase Proxy"

    @api.model
    def add_quantity(self, product_id, product_qty):
        ProductProduct = self.env["product.product"]
        PurchaseOrder = self.env["purchase.order"]
        PurchaseOrderLine = self.env["purchase.order.line"]

        product = ProductProduct.browse(product_id)
        if not product:
            print("ERROR to handle: product not found")
        if not product.seller_ids:
            print("ERROR to handle: sellers not found")
            return
        seller = product.seller_ids[0].name
        orders = PurchaseOrder.search([
            ('partner_id', '=', seller.id),
            ('state', '=', 'draft')], order="date_order desc")
        if not orders:
            order = PurchaseOrder.create({
                "partner_id": seller.id,
            })
        else:
            order = orders[0]
        line = PurchaseOrderLine.create({
            "order_id": order.id,
            "product_id": product.id,
            "product_qty": product_qty,
            "name": "name",
            "date_planned": "2020-01-01",
            "product_uom": product.uom_po_id.id,
            "price_unit": 0.0,
        })
        line.onchange_product_id()
