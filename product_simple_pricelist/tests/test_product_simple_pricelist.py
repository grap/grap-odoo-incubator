# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductSimplePricelist(TransactionCase):
    """Tests for 'Product - Simple Pricelist' Module"""

    def setUp(self):
        super(TestProductSimplePricelist, self).setUp()
        self.simple_item_obj = self.env['product.simple.pricelist.item']
        self.simple_pricelist = self.env.ref(
            'product_simple_pricelist.simple_pricelist')
        self.service_product = self.env.ref(
            'product.product_product_consultant')

    # Test Section
    def test_01_add_new_price(self):
        items = self.simple_item_obj.search([
            ('pricelist_id', '=', self.simple_pricelist.id),
            ('product_id', '=', self.service_product.id)])
        self.assertEqual(
            len(items), 1,
            "The simple pricelist item should display a line per product.")
        self.assertEqual(
            items[0].difference, 0,
            "Without any action, difference should be null.")
