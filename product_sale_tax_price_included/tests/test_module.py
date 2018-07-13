# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.product_template_demo_included = self.env.ref(
            'product_sale_tax_price_included.product_template_demo_included')
        self.product_template_demo_excluded = self.env.ref(
            'product_sale_tax_price_included.product_template_demo_excluded')
        self.product_template_demo_mixed = self.env.ref(
            'product_sale_tax_price_included.product_template_demo_mixed')
        self.product_template_demo_no_tax = self.env.ref(
            'product_sale_tax_price_included.product_template_demo_no_tax')

    # Test Section
    def test_01_test_product_fieds(self):
        # Test Product Tax Included
        self.assertEqual(
            self.product_template_demo_included.sale_tax_price_include,
            'all_tax_incl',
            "Incorrect selection for product with tax included.")
        self.assertEqual(
            self.product_template_demo_included.price_vat_excl, 250,
            "Incorrect price Excluded for product with tax included.")
        self.assertEqual(
            self.product_template_demo_included.price_vat_incl, 300,
            "Incorrect price Included for product with tax included.")

        # Test Product Tax Excluded
        self.assertEqual(
            self.product_template_demo_excluded.sale_tax_price_include,
            'all_tax_excl',
            "Incorrect selection for product with tax excluded.")
        self.assertEqual(
            self.product_template_demo_excluded.price_vat_excl, 300,
            "Incorrect price Excluded for product with tax excluded.")
        self.assertEqual(
            self.product_template_demo_excluded.price_vat_incl, 360,
            "Incorrect price Included for product with tax excluded.")

        # Test Product Mixed Taxes
        self.assertEqual(
            self.product_template_demo_mixed.sale_tax_price_include,
            'mixed_taxes',
            "Incorrect selection for product with mixed taxed.")

        # Test Product Mixed Taxes
        self.assertEqual(
            self.product_template_demo_no_tax.sale_tax_price_include,
            'no_tax',
            "Incorrect selection for product with no tax.")
        self.assertEqual(
            self.product_template_demo_no_tax.price_vat_excl, 300,
            "Incorrect price Excluded for product with no tax.")
        self.assertEqual(
            self.product_template_demo_no_tax.price_vat_incl, 300,
            "Incorrect price Included for product with no tax.")
