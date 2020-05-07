# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class MobileKioskPurchase(models.TransientModel):
    _name = "mobile.kiosk.purchase"
    _inherit = "mobile.kiosk.abstract"
    _description = "Mobile Kiosk Purchase Proxy"

    @api.model
    def select_partner(self, partner_id):
        """Create a purchase order, or select the last purchase order
        of a given partner"""
        result = self._prepare_result()

        # Get a Purchase Order, or create a new one
        self._select_purchase_order(partner_id, result)

        return result

    @api.model
    def select_product(self, partner_id, product_id):
        result = self._prepare_result()
        ProductProduct = self.env["product.product"]
        product = ProductProduct.browse([product_id])[0]
        self._select_product(partner_id, product, result)
        return result

    @api.model
    def scan_barcode(self, partner_id, barcode):
        result = self._prepare_result()
        ProductProduct = self.env["product.product"]

        # Get product or raise an error
        products = ProductProduct.search([("barcode", "=", barcode)])
        if not products:
            return self._add_result_error(
                result,
                "Barcode not found",
                _("No product has been found for barcode '%s'" % barcode),
            )
        product = products[0]
        self._select_product(partner_id, product, result)
        return result

    @api.model
    def add_quantity(self, purchase_order_id, product_id, product_qty):
        result = self._prepare_result()
        ProductProduct = self.env["product.product"]
        PurchaseOrder = self.env["purchase.order"]
        PurchaseOrderLine = self.env["purchase.order.line"]

        order = PurchaseOrder.browse(purchase_order_id)
        product = ProductProduct.browse(product_id)

        # TODO: FIXME
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
        line.product_qty = product_qty
        # line._onchange_quantity()
        return result

    @api.model
    def _select_purchase_order(self, partner_id, result):
        PurchaseOrder = self.env["purchase.order"]

        orders = PurchaseOrder.search([
            ("partner_id", "=", partner_id),
            ("state", "in", self._get_purchase_order_loadable_state())
        ], order="date_order desc")
        if not orders:
            order = PurchaseOrder.create({
                "partner_id": partner_id,
            })
            self._add_result_notify(
                result,
                _("Purchase Order created"),
                _("A new Purchase Order %s has been created" % (order.name))
            )
        else:
            order = orders[0]
        self._prepare_purchase_order_data(result, order)

    def _select_product(self, partner_id, product, result):
        self._prepare_product_data(result, product)

        # if not partner_id is defined, we get the first one
        if not partner_id:
            if not product.seller_ids:
                self._add_result_error(
                    result,
                    "Product without Supplier",
                    _("The select product doesn't have any supplier defined")
                )
                return
            else:
                partner_id = product.seller_ids[0].name.id
                result["partner_name"] = product.seller_ids[0].name.name
                self._select_purchase_order(partner_id, result)

        # Get Supplierinfo
        supplierinfos = product.seller_ids\
            .filtered(lambda r: r.name.id == partner_id and (
                not r.product_id or r.product_id.id == product.id))\
            .sorted(key=lambda r: r.min_qty)
        self._prepare_supplierinfo_data(
            result, supplierinfos and supplierinfos[0] or False)

    @api.model
    def _prepare_purchase_order_data(self, result, purchase_order):
        result.update({
            "purchase_order_id": purchase_order.id,
            "purchase_order_name": purchase_order.name,
        })

    @api.model
    def _get_purchase_order_loadable_state(self):
        return ["draft", "sent"]
