# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.MobileKioskInventory = cls.env["mobile.kiosk.inventory"]
        cls.StockInventory = cls.env["stock.inventory"]
        cls.ProductProduct = cls.env["product.product"]
        cls.product_1 = cls.env.ref("mobile_kiosk_abstract.product_1")
        cls.random_product = cls.env.ref("product.product_product_5")

    def _assert_notification(self, result, expected_level):
        self.assertIn(
            expected_level,
            [x.get("type") for x in result.get("notifications", [])],
            result,
        )

    def _get_context(self, result):
        self.assertIn("action", result.keys(), result)
        self.assertNotEqual(result.get("action"), False, result)
        self.assertIn("context", result["action"].keys(), result)
        return result["action"]["context"]

    def _get_context_value(self, result, context_key):
        context = self._get_context(result)
        self.assertIn(context_key, context, result)
        return context[context_key]

    def _get_context_value_from_action(self, action, context_key):
        self.assertIn("context", action.keys(), action)
        context = action["context"]
        self.assertIn(context_key, context, action)
        return context[context_key]

    def test_full_workflow_mobile_kiosk_inventory(self):
        inventory_name = "Test Inventory"

        # [API::create_inventory] Create a New Inventory without inventory name
        result = self.MobileKioskInventory.create_inventory("")
        self._assert_notification(result, "danger")

        # [API::create_inventory] Create a New Inventory
        result = self.MobileKioskInventory.create_inventory(inventory_name)
        inventory_context = self._get_context(result)
        self._assert_notification(result, "info")

        inventory_id = self._get_context_value(result, "mk_inventory_inventory_id")
        inventory = self.StockInventory.browse(inventory_id)

        # [API::mk_inventory_stock_inventory_select] Select an existing Inventory
        result = inventory.mk_inventory_stock_inventory_select()
        self.assertEqual(
            self._get_context_value_from_action(result, "mk_inventory_inventory_name"),
            inventory_name,
            "Select an inventory should return the existing one.",
        )

        # [API::scan_barcode] incorrect barcode
        result = self.MobileKioskInventory.with_context(
            **inventory_context
        ).scan_barcode("BAD BARCODE")
        self._assert_notification(result, "danger")

        # [API::scan_barcode] Correct barcode
        result = self.MobileKioskInventory.with_context(
            **inventory_context
        ).scan_barcode("3701078243449")
        product_context = self._get_context(result)
        self.assertEqual(
            self._get_context_value(result, "mk_inventory_product_name"),
            self.product_1.name,
            "Scan a product should return its name.",
        )

        # [API::mk_inventory_product_product_select] Select an existing Product
        result = self.random_product.mk_inventory_product_product_select()
        self.assertEqual(
            self._get_context_value_from_action(result, "mk_inventory_product_name"),
            self.random_product.name,
            "Select an Product should return the existing one.",
        )

        # [API::add_quantity]
        self.MobileKioskInventory.with_context(**product_context).add_quantity(
            inventory_id, self.product_1.id, 15.0
        )
        self.assertEqual(
            len(inventory.line_ids),
            1,
            "Add quantity should add a new line on inventory.",
        )
        self.assertEqual(
            inventory.line_ids[0].product_qty,
            15.0,
            "Add quantity should add a new line on inventory"
            " with the according quantity.",
        )

        # [API::add_quantity] Duplicate quantity
        self.MobileKioskInventory.with_context(**product_context).add_quantity(
            inventory_id, self.product_1.id, 20.0
        )

        self.assertEqual(
            len(inventory.line_ids),
            1,
            "Readd quantity should not create a new line on inventory.",
        )

        self.assertEqual(
            inventory.line_ids[0].product_qty,
            35.0,
            "ReAdd quantity should add change the existing line, suming quantity.",
        )
