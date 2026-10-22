# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import tagged

from odoo.addons.mobile_kiosk_abstract.tests.test_abstract import TestAbstract


@tagged("post_install", "-at_install")
class TestModule(TestAbstract):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.MobileKioskPurchase = cls.env["mobile.kiosk.purchase"]
        cls.PurchaseOrder = cls.env["purchase.order"]

    def test_full_workflow_mobile_kiosk_purchase(self):
        # [API::mk_purchase_res_partner_select] Select an existing Partner
        result = self.supplier.mk_purchase_res_partner_select()
        purchase_context = self._get_context_from_action(result)
        self.assertEqual(
            self._get_context_value_from_action(result, "mk_purchase_supplier_name"),
            self.supplier.name,
            "Select a supplier should return the existing one.",
        )

        # [API::mk_purchase_product_product_select] Select an existing Product
        result = self.random_product.with_context(
            **purchase_context
        ).mk_purchase_product_product_select()
        self.assertEqual(
            self._get_context_value_from_action(result, "mk_purchase_supplier_name"),
            self.supplier.name,
            "Select an Product should return partner information.",
        )
        self.assertEqual(
            self._get_context_value_from_action(result, "mk_purchase_product_name"),
            self.random_product.name,
            "Select an Product should return the existing one.",
        )

        # [API::scan_barcode] incorrect barcode
        result = self.MobileKioskPurchase.with_context(**purchase_context).scan_barcode(
            "BAD BARCODE", self.supplier.id
        )
        self._assert_notification(result, "danger")

        # [API::scan_barcode] Correct barcode
        result = self.MobileKioskPurchase.with_context(**purchase_context).scan_barcode(
            self.product_1.barcode, self.supplier.id
        )
        purchase_context = self._get_context(result)
        self.assertEqual(
            self._get_context_value(result, "mk_purchase_product_name"),
            self.product_1.name,
            "Scan a product should return its name.",
        )

        # [API::add_quantity]
        self.assertEqual(
            len(self.PurchaseOrder.search([("partner_id", "=", self.supplier.id)])), 0
        )
        self.MobileKioskPurchase.with_context(**purchase_context).add_quantity(
            self.supplier.id, self.product_1.id, 50.0
        )
        purchase = self.PurchaseOrder.search([("partner_id", "=", self.supplier.id)])
        self.assertEqual(
            len(purchase),
            1,
            "Adding a quantity for a supplier that doesn't have any purchase order"
            " should create a purchase order",
        )
        self.assertEqual(
            len(purchase.order_line),
            1,
            "Add quantity should add a new line on purchase order.",
        )
        self.assertEqual(
            purchase.order_line[0].product_qty,
            50.0,
            "Add quantity should add a new line on purchase order"
            " with the according quantity.",
        )

        # [API::add_quantity] Duplicate product with quantity to round
        self.MobileKioskPurchase.with_context(**purchase_context).add_quantity(
            self.supplier.id, self.product_1.id, 61.0
        )

        self.assertEqual(
            len(purchase.order_line),
            2,
            "Readd quantity should create a new line on purchase order.",
        )
        self.assertEqual(
            sorted(purchase.mapped("order_line.product_qty")),
            [50.0, 70.0],
            "Add incorrect quantity should round the quantity"
            " according the multiplier setting.",
        )

        # [API::add_quantity] New product with insufficiant quantity
        self.MobileKioskPurchase.with_context(**purchase_context).add_quantity(
            self.supplier.id, self.product_2.id, 4.0
        )

        self.assertEqual(
            len(purchase.order_line),
            3,
            "Add quantity for new product should create a new line on purchase order.",
        )
        self.assertEqual(
            sorted(purchase.mapped("order_line.product_qty")),
            [10.0, 50.0, 70.0],
            "Add insufficiant quantity should round the quantity"
            " according the minimum quantity setting.",
        )
