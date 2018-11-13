# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.ProductCategory = self.env['product.category']
        self.category_parent = self.env.ref(
            'product_categ_search_complete_name.category_parent')
        self.category_child = self.env.ref(
            'product_categ_search_complete_name.category_child')

    # Test Section
    def test_01_search_category_complete(self):
        res = self.ProductCategory.name_search(
            self.category_child.complete_name)

        self.assertEqual(
            len(res) == 1 and res[0][0],
            self.category_child.id,
            "Searching on complete name should succeed")

    # Test Section
    def test_02_search_category_partial(self):
        res = self.ProductCategory.name_search(
            "%s /" % self.category_parent.name)

        self.assertEqual(
            len(res) == 1 and res[0][0],
            self.category_child.id,
            "Searching on the name of the parent plus / should succeed")
