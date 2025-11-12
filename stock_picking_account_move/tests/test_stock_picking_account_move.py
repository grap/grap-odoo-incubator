# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.tests.common import TransactionCase


class TestStockPickingAccountMove(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AccountMoveLine = cls.env["account.move.line"]

        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")

        cls.expense_account = cls.env["account.account"].create(
            {
                "name": "Test Expense Account",
                "code": "600EXP",
                "account_type": "expense",
                "company_id": cls.env.company.id,
            }
        )
        cls.transfert_account = cls.env["account.account"].create(
            {
                "name": "Test Transfer Account ",
                "code": "600TRANS",
                "account_type": "expense",
                "company_id": cls.env.company.id,
            }
        )
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Test Journal2",
                "type": "general",
                "code": "TEST2",
                "company_id": cls.env.company.id,
            }
        )
        cls.tax = cls.env["account.tax"].create(
            {
                "name": "Test Purchase Tax 20%",
                "amount": 20.0,
                "type_tax_use": "purchase",
            }
        )

        cls.product_without_tax = cls.env["product.product"].create(
            {
                "name": "Product Without Tax",
                "type": "product",
                "standard_price": 10,
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "categ_id": cls.env.ref("product.product_category_all").id,
                "supplier_taxes_id": [],
                "property_account_expense_id": cls.expense_account.id,
            }
        )

        cls.product_with_tax = cls.env["product.product"].create(
            {
                "name": "Product With Tax",
                "type": "product",
                "standard_price": 100,
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "categ_id": cls.env.ref("product.product_category_all").id,
                "supplier_taxes_id": [Command.set(cls.tax.ids)],
                "property_account_expense_id": cls.expense_account.id,
            }
        )

        cls.picking_type = cls.env["stock.picking.type"].create(
            {
                "name": "Internal Use Case 2",
                "default_location_src_id": cls.env.ref(
                    "stock.stock_location_suppliers"
                ).id,
                "default_location_dest_id": cls.env.ref(
                    "stock.stock_location_stock"
                ).id,
                "sequence_code": "TST2",
                "journal_id": cls.journal.id,
                "account_id": cls.transfert_account.id,
                "show_operations": False,
            }
        )

        cls.picking = cls.env["stock.picking"].create(
            {
                "picking_type_id": cls.picking_type.id,
                "location_id": cls.picking_type.default_location_src_id.id,
                "location_dest_id": cls.picking_type.default_location_dest_id.id,
            }
        )

        cls.move_A_1 = cls.env["stock.move"].create(
            {
                "name": "Test Move A 1",
                "picking_id": cls.picking.id,
                "product_id": cls.product_without_tax.id,
                "location_id": cls.picking.location_id.id,
                "location_dest_id": cls.picking.location_dest_id.id,
                "product_uom_qty": 1,
                "product_uom": cls.uom_unit.id,
            }
        )
        cls.move_A_2 = cls.env["stock.move"].create(
            {
                "name": "Test Move A 2",
                "picking_id": cls.picking.id,
                "product_id": cls.product_without_tax.id,
                "location_id": cls.picking.location_id.id,
                "location_dest_id": cls.picking.location_dest_id.id,
                "product_uom_qty": 1,
                "product_uom": cls.uom_dozen.id,
            }
        )
        cls.move_B = cls.env["stock.move"].create(
            {
                "name": "Test Move B",
                "picking_id": cls.picking.id,
                "product_id": cls.product_with_tax.id,
                "location_id": cls.picking.location_id.id,
                "location_dest_id": cls.picking.location_dest_id.id,
                "product_uom_qty": 33,
                "product_uom": cls.uom_unit.id,
            }
        )

    def _mark_picking_as_done(self):
        self.picking.action_confirm()
        for move in self.picking.move_ids:
            move.move_line_ids[0].qty_done = move.product_uom_qty
        self.picking.button_validate()

    def _assert_move_line(self, move, **kwargs):
        domain = [("move_id", "=", move.id)] + [
            (x, "=", kwargs[x]) for x in kwargs.keys() if x != "tax_ids"
        ]
        lines = self.AccountMoveLine.search(domain)

        self.assertEqual(len(lines), 1, f"Account move line not found {domain}")
        if "tax_ids" in kwargs.keys():
            self.assertEqual(lines.mapped("tax_ids").ids, kwargs["tax_ids"])

    def test_01_accounting_state(self):
        self.assertEqual(self.picking.state, "draft")
        self.assertEqual(self.picking.account_move_state, "waiting")
        self._mark_picking_as_done()
        self.assertEqual(self.picking.account_move_state, "to_do")
        self.picking.picking_type_id.write(
            {
                "journal_id": False,
                "account_id": False,
            }
        )
        self.assertEqual(self.picking.account_move_state, "no_need")

    def test_02_generate_account_move(self):
        self._mark_picking_as_done()
        self.assertFalse(self.picking.account_move_id)
        self.picking.generate_account_move()
        self.assertEqual(self.picking.account_move_state, "done")
        self.assertTrue(self.picking.account_move_id)
        self.assertEqual(self.picking.account_move_id.state, "posted")

        move = self.picking.account_move_id
        # Check counter product move lines
        self._assert_move_line(
            move,
            account_id=self.expense_account.id,
            credit=(1 + 12) * 10,
            tax_ids=[],
        )
        self._assert_move_line(
            move,
            account_id=self.expense_account.id,
            credit=33 * 100,
            tax_ids=self.tax.ids,
        )

        # Check transfert move lines
        self._assert_move_line(
            move,
            account_id=self.transfert_account.id,
            debit=(1 + 12) * 10,
            tax_ids=[],
        )
        self._assert_move_line(
            move,
            account_id=self.transfert_account.id,
            debit=33 * 100,
            tax_ids=self.tax.ids,
        )

    # def test_03_inversed_account_move(self):
    #     """Test that the return picking is well created with new field is_return"""
    #     wiz = (
    #         self.env["stock.return.picking"]
    #         .with_context(active_id=self.picking.id, active_model="stock.picking")
    #         .create({})
    #     )
    #     wiz._onchange_picking_id()
    #     picking_returned_id = wiz._create_returns()[0]
    #     picking_returned = self.Picking.browse(picking_returned_id)
    #     self.assertEqual(
    #         picking_returned.is_return, True, "Picking return should be True"
    #     )