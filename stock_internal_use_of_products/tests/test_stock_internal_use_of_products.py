# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestStockInternalUseOfProducts(TransactionCase):
    """Tests for 'Stock - Internal Use of Products' Module"""

    def setUp(self):
        super().setUp()
        self.AccountMoveLine = self.env['account.move.line']
        self.product_dozen = self.env.ref('product.product_product_6')
        self.regular_expense_account = self.env.ref(
            'stock_internal_use_of_products.regular_expense_account')
        self.use_expense_account = self.env.ref(
            'stock_internal_use_of_products.use_expense_account')
        self.internal_use = self.env.ref(
            'stock_internal_use_of_products.internal_use')
        self.internal_use_without = self.env.ref(
            'stock_internal_use_of_products.internal_use_without')

    # Test Section
    def test_01_stock_move_without_account_move(self):
        # Stock Check
        self.internal_use_without.action_confirm()
        self.assertEqual(
            self.internal_use_without.state, 'done',
            "Confirming internal use without accounting setting should set"
            " the internal use in a 'done' state")

    # Test Section
    def test_02_stock_move_and_account_move(self):
        # Stock Check
        self.internal_use.action_confirm()
        self.assertEqual(
            len(self.internal_use.stock_move_ids), 3,
            "Confirm an Internal use with 3 lines should create 3 stock moves")

        dozen_moves = self.internal_use.stock_move_ids.filtered(
            lambda x: x.product_id == self.product_dozen)
        self.assertEqual(
            len(dozen_moves), 1,
            "Each use line should generate one unique move line")
        self.assertEqual(
            dozen_moves[0].product_qty, 3 * 12,
            "Stock move quantity should be expressed in the product UoM")

        self.assertEqual(
            self.internal_use.state, 'confirmed',
            "Confirming internal use should change its state")

        # Accounting Check
        self.internal_use.action_done()
        self.assertNotEqual(
            self.internal_use.account_move_id, False,
            "Finish an Internal use should generate an accounting entry")
        self.assertEqual(
            len(self.internal_use.account_move_id.line_ids), 4,
            "Internal use with 3 lines including one with tax should generate"
            " an accouting entry with 4 lines")

        # # Check Line 1 (Charge 1) (merged lines without tax code)
        # lines = self.AccountMoveLine.search([
        #     ('move_id', '=', self.internal_use.account_move_id.id),
        #     ('tax_ids', '=', False),
        #     ('credit', '=', (3 * 12 * 13) + 876),
        #     ('account_id', '=', self.regular_expense_account.id),
        # ])
        # self.assertEqual(
        #     len(lines), 1,
        #     "many use lines should generate account single accounting move")

        # # Check Line 2 (Charge 2) (line with tax code)
        # lines = self.AccountMoveLine.search([
        #     ('move_id', '=', self.internal_use.account_move_id.id),
        #     ('credit', '=', 20),
        #     ('account_id', '=', self.regular_expense_account.id),
        # ])
        # self.assertEqual(
        #     len(lines), 1,
        #     "Lines with tax code should generated"
        #     " separated account move line")

        # Check Line 3 (Uncharge lines)
        lines = self.AccountMoveLine.search([
            ('move_id', '=', self.internal_use.account_move_id.id),
            ('account_id', '=', self.use_expense_account.id),
        ])
        self.assertEqual(
            len(lines), 2,
            "Incorrect uncharge account move line.")
