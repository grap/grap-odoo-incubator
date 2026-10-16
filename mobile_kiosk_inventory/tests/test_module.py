# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.MobileKioskInventory = self.env["mobile.kiosk.inventory"]
        self.StockInventory = self.env["stock.inventory"]
        self.partner = self.env.ref(
            "mobile_kiosk_abstract.mobile_kiosk_partner_supplier"
        )
        self.product_1 = self.env.ref("mobile_kiosk_abstract.mobile_kiosk_product_1")
        self.random_product = self.env.ref("product.product_product_4d")

    def test_full_workflow_mobile_kiosk_inventory(self):
        inventory_name = "Test Inventory"

        # [API::create_inventory] Create a New Inventory
        create_inventory_result = self.MobileKioskInventory.create_inventory(
            inventory_name
        )
        inventory_id = create_inventory_result.get("inventory_id", False)
        self.assertNotEqual(
            inventory_id, False, "Create a new inventory should create a new one."
        )
        inventory = self.StockInventory.browse(inventory_id)

        # [API::select_inventory] Select an existing Inventory
        select_inventory_result = self.MobileKioskInventory.select_inventory(
            inventory_id
        )
        self.assertEqual(
            select_inventory_result.get("inventory_name", False),
            inventory_name,
            "Select an inventory should return the existing one.",
        )

        # [API::select_product]
        select_product_result = self.MobileKioskInventory.select_product(
            self.random_product.id
        )
        self.assertEqual(
            select_product_result.get("product_name", False),
            self.random_product.name,
            "Select an product should return its name.",
        )

        # [API::scan_barcode]
        scan_barcode_result = self.MobileKioskInventory.select_product(
            self.product_1.id
        )
        self.assertEqual(
            scan_barcode_result.get("product_name", False),
            self.product_1.name,
            "Scan a product should return its name.",
        )

        # [API::add_quantity]
        self.MobileKioskInventory.add_quantity(
            inventory_id,
            self.product_1.id,
            15.0,
        )
        self.assertEqual(
            len(inventory.line_ids),
            1,
            "Add quantity should add a new line on inventory.",
        )
        self.assertEqual(
            inventory.line_ids[0].product_qty,
            15.0,
            "Add quantity should add a new line on inventory with the according quantity.",
        )

        self.MobileKioskInventory.add_quantity(
            inventory_id,
            self.product_1.id,
            20.0,
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
