# coding: utf-8
# Copyright (C) 2018-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


class TestModule(common.TransactionCase):
    def setUp(self):
        super(TestModule, self).setUp()
        self.MobileAppPurchase = self.env["mobile.app.purchase"]
        self.PurchaseOrder = self.env["purchase.order"]
        self.supplier = self.env.ref("base.res_partner_1")
        self.product = self.env.ref("mobile_app_purchase.product_evian")

    def test_01_scenario_call_api_without_test(self):
        self.MobileAppPurchase.get_purchase_orders()
        self.MobileAppPurchase.get_partners()
        self.MobileAppPurchase.get_products(
            {"purchase_order": {"partner": {"id": self.supplier.id}}}
        )
        self.MobileAppPurchase.get_products(
            {
                "purchase_order": {"partner": {"id": self.supplier.id}},
                "barcode": "3068320063003",
            }
        )

    def test_02_scenario_add_line(self):
        # Create new purchase order
        order_data = self.MobileAppPurchase.create_purchase_order(
            {"partner": {"id": self.supplier.id}}
        )
        order = self.PurchaseOrder.browse(order_data.get("id", False))
        self.assertNotEqual(order.id, False, "Purchase Order Creation failed")

        # Add new line to existing command
        order_data = self.MobileAppPurchase.add_purchase_order_line(
            {
                "purchase_order": {"id": order.id},
                "product": {"id": self.product.id},
                "qty": 50,
            }
        )
        self.assertEqual(
            len(order.order_line), 1, "Purchase Order Line Creation failed"
        )
