# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import Warning as UserError
from odoo.tests.common import TransactionCase


class TestStockInventoryMerge(TransactionCase):
    def setUp(self):
        super(TestStockInventoryMerge, self).setUp()
        self.inventory_obj = self.env["stock.inventory"]
        self.line_obj = self.env["stock.inventory.line"]
        self.wizard_obj = self.env["wizard.stock.inventory.merge"]
        self.StockTrackConfirmation = self.env["stock.track.confirmation"]
        self.inventory_1 = self.env.ref("stock_inventory_merge.inventory_1")
        self.stock_location = self.env.ref("stock.stock_location_stock")
        self.component_location = self.env.ref("stock.stock_location_components")
        self.line_1_1 = self.env.ref("stock_inventory_merge.inventory_line_1_1")
        self.line_1_2 = self.env.ref("stock_inventory_merge.inventory_line_1_2")
        self.inventory_2 = self.env.ref("stock_inventory_merge.inventory_2")
        self.ipad_product = self.env.ref("product.product_product_6")

    def _confirm_inventory(self, inventory):
        result = inventory.action_validate()
        if result:
            lot_wizard = self.StockTrackConfirmation.browse(result["res_id"])
            lot_wizard.action_confirm()

    # Test Section
    def test_01_block_done_inventory(self):
        with self.assertRaises(UserError):
            self._confirm_inventory(self.inventory_1)

    def test_02_merge_duplicated_lines(self):
        to_merge_line_ids = [self.line_1_1.id, self.line_1_2.id]
        self.inventory_1.action_merge_duplicated_line()
        self.assertEqual(
            len(self.inventory_1.line_ids),
            2,
            "Merging duplicated lines should delete lines.",
        )
        lines = self.inventory_1.line_ids.search([("id", "in", to_merge_line_ids)])
        self.assertEqual(
            len(lines),
            1,
            "Merging duplicated lines should have deleted duplicated lines.",
        )
        self.assertEqual(
            round(lines[0].product_qty * lines[0].product_uom_id.factor_inv),
            32,
            "Merging 20 Units and 1 Dozen quantity should return 32 Units.",
        )

    def test_03_merge_inventories(self):
        inventory_name = "Test Merged Inventory"
        to_merge_inventory = [self.inventory_1, self.inventory_2]
        to_merge_inventory_ids = []

        # Start inventories
        for inventory in to_merge_inventory:
            to_merge_inventory_ids.append(inventory.id)
            inventory.action_start()

        wizard = self.wizard_obj.with_context(
            active_ids=to_merge_inventory_ids,
            active_model="stock.inventory",
        ).create({"name": inventory_name})
        wizard.action_merge()

        inventories = self.inventory_obj.search([("id", "in", to_merge_inventory_ids)])
        self.assertEqual(
            len(inventories),
            2,
            "Merge Wizard Inventories should not delete inventories.",
        )
        new_inventory = self.inventory_obj.search([("name", "=", inventory_name)])
        self.assertEqual(
            len(new_inventory.line_ids),
            len(inventories.mapped("line_ids")),
            "Merging 2 inventories should create a new one with the lines."
            " of all the merged inventories.",
        )

    def test_04_fill_with_zero(self):
        new_inventory_1 = self.inventory_obj.create(
            {
                "name": "TEST #1",
                "filter": "partial",
                "location_id": self.stock_location.id,
            }
        )
        new_inventory_1.action_start()
        new_inventory_2 = new_inventory_1.copy(default={"name": "TEST #2"})
        self.line_obj.create(
            {
                "product_id": self.ipad_product.id,
                "location_id": self.component_location.id,
                "inventory_id": new_inventory_2.id,
            }
        )
        new_inventory_2.action_start()
        new_inventory_1.complete_with_zero()
        new_inventory_2.complete_with_zero()

        self.assertEqual(
            len(new_inventory_1.line_ids),
            len(new_inventory_2.line_ids),
            "complete an empty and a non empty inventory should return the"
            " same product list",
        )

        # We confirm an inventory that set all product to 0
        self._confirm_inventory(new_inventory_1)

        new_inventory_3 = self.inventory_obj.create(
            {
                "name": "TEST #3",
                "filter": "partial",
                "location_id": self.stock_location.id,
            }
        )
        new_inventory_3.action_start()
        new_inventory_3.complete_with_zero()
        self.assertEqual(
            len(new_inventory_3.line_ids),
            0,
            "If stock are null, complete with 0 process should not add lines.",
        )
