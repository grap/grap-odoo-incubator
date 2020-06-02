# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestStockInventoryMerge(TransactionCase):
    def setUp(self):
        super(TestStockInventoryMerge, self).setUp()
        self.inventory_obj = self.env["stock.inventory"]
        self.inventory_1 = self.env.ref(
            "stock_inventory_valuation.inventory_1"
        )
        self.line_1_1 = self.env.ref(
            "stock_inventory_valuation.inventory_line_1_1"
        )

    # Test Section
    def test_01_compute_valuation(self):

        self.assertEqual(
            self.line_1_1.valuation,
            11,
            "Valuation of this line should be 11",
        )
