# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestStockInternalUseOfProducts(TransactionCase):
    """Tests for 'Stock - Internal Use of Products' Module"""

    def setUp(self):
        super(TestStockInternalUseOfProducts, self).setUp()
        self.internal_use = self.env.ref(
            'stock_internal_use_of_products.internal_use')
        self.product_dozen = self.env.ref(
            'product.product_product_48')

    # Test Section
    def test_01_stock_move_and_account_move(self):
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
