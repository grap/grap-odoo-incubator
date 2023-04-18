# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


# @at_install(False)
# @post_install(True)
class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.MobileKioskPurchase = self.env["mobile.kiosk.purchase"]
        self.PurchaseOrder = self.env["purchase.order"]
        self.partner = self.env.ref(
            "mobile_kiosk_abstract.mobile_kiosk_partner_supplier"
        )
        self.product_1 = self.env.ref("mobile_kiosk_abstract.mobile_kiosk_product_1")
        self.product_2 = self.env.ref("mobile_kiosk_abstract.mobile_kiosk_product_2")
        self.random_product = self.env.ref("product.product_product_4d")

    def test_full_workflow_mobile_kiosk_purchase(self):
        # [API::select_partner] Select products via the UI
        select_partner_result = self.MobileKioskPurchase.select_partner(self.partner.id)
        self.assertEqual(
            select_partner_result.get("messages", [{}])[0].get("title", {}),
            "Purchase Order created",
            "Select a partner should create a new purchase order",
        )
        order = self.PurchaseOrder.browse(select_partner_result["purchase_order_id"])

        select_partner_result = self.MobileKioskPurchase.select_partner(self.partner.id)
        self.assertEqual(
            len(select_partner_result.get("messages", [{}])),
            0,
            "ReSelect a partner should not create a new purchase order",
        )

        # [API::select_product] Select products via the UI
        select_product_result = self.MobileKioskPurchase.select_product(
            self.partner.id, self.product_1.id
        )

        self.assertNotEqual(
            select_product_result.get("supplierinfo_uom_po_id", False),
            False,
            "Select a product related to the supplier should return a UoM",
        )
        select_product_result = self.MobileKioskPurchase.select_product(
            self.partner.id, self.random_product.id
        )

        self.assertEqual(
            select_product_result.get("supplierinfo_uom_po_id", False),
            False,
            "Select a product unrelated to the supplier should NOT return a UoM",
        )

        # [API::scan_barcode] Select products via barcode
        scan_barcode_result = self.MobileKioskPurchase.scan_barcode(
            self.partner.id, self.product_1.barcode
        )
        self.assertEqual(
            scan_barcode_result.get("product_id", False),
            self.product_1.id,
            "Scan a barcode should return the Product",
        )

        scan_barcode_result = self.MobileKioskPurchase.scan_barcode(
            self.partner.id, "999"
        )
        self.assertEqual(
            scan_barcode_result.get("product_id", False),
            False,
            "Scan a non existing barcode should return nothing",
        )

        # [API::add_quantity] Add a quantity
        correct_qty = self.product_1.seller_ids[0].min_qty
        add_quantity_result = self.MobileKioskPurchase.add_quantity(
            order.id, self.product_1.id, correct_qty / 2
        )

        self.assertEqual(
            add_quantity_result.get("messages", [{}])[0].get("title", {}),
            "Quantity increased",
            "Quantity should be increased if the selected quantity is not enough",
        )

        self.assertEqual(
            len(order.order_line), 1, "Add quantity should create a new line"
        )
        self.assertEqual(
            order.order_line.product_qty,
            correct_qty,
            "Quantity on Line should be increased if the selected quantity is not enough",
        )

        self.MobileKioskPurchase.add_quantity(
            order.id, self.product_1.id, 2 * correct_qty
        )
        self.assertEqual(
            len(order.order_line),
            2,
            "ReAdd quantity for the same product should create a new line",
        )
