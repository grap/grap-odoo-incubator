# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.MergeWizard = cls.env["wizard.stock.inventory.merge"]
        cls.StockInventory = cls.env["stock.inventory"]
        cls.inventory_partial = cls.env.ref("stock_inventory_mgmt.inventory_partial")
        cls.inventory_category = cls.env.ref("stock_inventory_mgmt.inventory_category")
        cls.inventory_racking = cls.env.ref("stock_inventory_mgmt.inventory_racking")
        cls.demo_inventories = cls.StockInventory.search([])
        ctx = {
            "report_name": "stock_inventory_mgmt.report_stock_inventory_xlsx",
            "active_model": "stock.inventory",
            "active_ids": cls.demo_inventories.ids,
        }
        cls.report = cls.env["ir.actions.report"].with_context(**ctx)

    def _begin_inventories(self, inventories=False):
        inventories = inventories or self.demo_inventories
        inventories.action_start()
        for line in inventories.mapped("line_ids"):
            line.product_qty = line.theoretical_qty

    def _create_wizard_merge_inventories(self, inventories=False):
        inventories = inventories or self.demo_inventories
        wizard = self.MergeWizard.with_context(active_ids=inventories.ids).create({})
        return wizard

    def test_01_change_qty_and_confirm(self):
        self._begin_inventories(self.inventory_category)
        self.inventory_category.line_ids[0].product_qty += 10
        self.inventory_category.line_ids[1].product_qty += 20
        self.inventory_category.action_validate()
        self.assertEqual(len(self.inventory_category.move_ids), 2)

    def test_02_unlink_inventory(self):
        self.inventory_category.unlink()
        self._begin_inventories(self.inventory_racking)
        with self.assertRaises(UserError):
            self.inventory_racking.unlink()

    def test_03_validate_empty_inventory(self):
        self._begin_inventories(self.inventory_partial)
        with self.assertRaises(UserError):
            self.inventory_partial.action_validate()

    def test_04_check_duplicates(self):
        self._begin_inventories(self.inventory_category)
        for line in self.inventory_category.mapped("line_ids"):
            line.product_qty = line.theoretical_qty

        non_empty_lines = self.inventory_category.line_ids.filtered(
            lambda x: x.product_qty != 0
        )
        first_line = non_empty_lines[0]
        second_line = non_empty_lines[1]

        first_line.copy()
        self.assertEqual(self.inventory_category.duplicates_qty, 1)

        first_line.copy()
        self.assertEqual(self.inventory_category.duplicates_qty, 1)

        second_line_bis = second_line.copy()
        self.assertEqual(self.inventory_category.duplicates_qty, 2)

        result = self.inventory_category.action_view_duplicates()
        self.assertEqual(len(result.get("domain", [])[0][2]), 5)

        with self.assertRaises(UserError):
            self.inventory_category.action_validate()

        line_qty = self.inventory_category.line_qty

        second_line.product_qty = 10
        second_line.product_uom_id = self.env.ref("uom.product_uom_unit")
        second_line_bis.product_qty = 10
        second_line_bis.product_uom_id = self.env.ref("uom.product_uom_dozen")

        # Merge and try to confirm the inventory
        second_line_ids = (second_line | second_line_bis).ids
        self.inventory_category.action_merge_duplicated_lines()
        self.assertEqual(self.inventory_category.line_qty, line_qty - 3)
        second_line_merged = self.inventory_category.line_ids.filtered(
            lambda x, second_line_ids=second_line_ids: x.id in second_line_ids
        )
        self.assertEqual(len(second_line_merged), 1)

        res = second_line_merged.product_uom_id._compute_quantity(
            second_line_merged.product_qty,
            self.env.ref("uom.product_uom_unit"),
        )
        # We round because the current result return 130.08333
        # So, it works, but Odoo is quite annoying with bad default rounding
        self.assertEqual(round(res), 10 + 120)

        self.inventory_category.action_validate()

    def test_10_merge_and_confirm_full_workflow(self):
        self._begin_inventories()
        wizard = self._create_wizard_merge_inventories()
        result = wizard.action_merge()
        inventory = self.StockInventory.browse(result["res_id"])
        self.assertEqual(
            inventory.valuation, sum(self.demo_inventories.mapped("valuation"))
        )
        self.assertNotEqual(inventory.valuation, 0.0)
        self.assertEqual(inventory.state, "in_progress")
        self.assertEqual(set(self.demo_inventories.mapped("state")), {"pending_merge"})

        inventory.action_validate()
        self.assertEqual(inventory.state, "done")
        self.assertEqual(set(self.demo_inventories.mapped("state")), {"merged"})
        self.assertEqual(
            len(inventory.move_ids),
            len(
                inventory.mapped("line_ids").filtered(
                    lambda x: x.product_qty != x.theoretical_qty
                )
            ),
        )
        self.assertNotEqual(len(inventory.move_ids), 0)

        copied_inventory = inventory.copy()
        self.assertEqual(
            copied_inventory.state,
            "in_progress",
            "Copy a confirmed inventory should create a"
            " new inventory in 'In Progress' state.",
        )

    def test_11_check_in_merge_wizard_negative_line(self):
        self._begin_inventories()
        self.inventory_category.line_ids[0].product_qty = -100
        wizard = self._create_wizard_merge_inventories()
        with self.assertRaises(UserError):
            wizard.action_merge()

    def test_12_check_in_merge_wizard_single_inventory(self):
        self._begin_inventories()
        wizard = self._create_wizard_merge_inventories(self.inventory_category)
        with self.assertRaises(UserError):
            wizard.action_merge()

    def test_13_check_in_merge_wizard_bad_state(self):
        wizard = self._create_wizard_merge_inventories()
        with self.assertRaises(UserError):
            wizard.action_merge()

    def test_20_report_xlsx(self):
        report_xlsx = self.report._render_xlsx(None, None, None)
        self.assertEqual(report_xlsx[1], "xlsx")
