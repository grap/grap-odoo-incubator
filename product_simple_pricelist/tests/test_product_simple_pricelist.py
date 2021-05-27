# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    """Tests for 'Product - Simple Pricelist' Module"""

    def setUp(self):
        super().setUp()
        self.ProductPricelistItem = self.env["product.pricelist.item"]
        self.simple_pricelist = self.env.ref(
            "product_simple_pricelist.pricelist_editable_based_default"
        )
        self.simple_recursive_pricelist = self.env.ref(
            "product_simple_pricelist.pricelist_editable_based_discount"
        )
        self.corner_desk_product = self.env.ref("product.product_product_5")

    # Test Section
    def test_01_add_new_price(self):
        product = self.corner_desk_product.with_context(
            pricelist_id=self.simple_pricelist.id
        )
        self.assertEqual(
            product.lst_price,
            product.pricelist_price,
            "By default, pricelist price should be the same as list price.",
        )

        product.pricelist_price = product.lst_price / 2

        product._compute_pricelist_price()
        self.assertEqual(
            product.pricelist_price_difference_rate,
            -50.0,
            "bad computation of the pricelist differente rate",
        )
        items = self.ProductPricelistItem.search(
            [
                ("pricelist_id", "=", self.simple_pricelist.id),
                ("product_id", "=", product.id),
            ]
        )
        self.assertEqual(
            len(items), 1, "apply pricelist price should create a pricelist item"
        )

        product.delete_pricelist_price()
        items = self.ProductPricelistItem.search(
            [
                ("pricelist_id", "=", self.simple_pricelist.id),
                ("product_id", "=", product.id),
            ]
        )
        self.assertEqual(
            len(items),
            0,
            "Delete pricelist price should delete the pricelist item",
        )

    def test_02_sub_pricelist(self):
        product = self.corner_desk_product.with_context(
            pricelist_id=self.simple_recursive_pricelist.id
        )
        self.assertEqual(
            product.lst_price * 0.9,
            product.pricelist_price,
            "By default, pricelist price should be the default discount price (-10%).",
        )

        product.pricelist_price = product.lst_price / 2
        product._compute_pricelist_price()
        self.assertEqual(
            product.pricelist_price_difference_rate,
            -50.0,
            "bad computation of the pricelist differente rate",
        )
