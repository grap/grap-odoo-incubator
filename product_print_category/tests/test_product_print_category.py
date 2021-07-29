# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductPrintCategory(TransactionCase):
    """Tests for 'Product Print Category' Module"""

    def setUp(self):
        super().setUp()
        self.ProductPrintWizard = self.env["product.print.wizard"]
        self.ProductProduct = self.env["product.product"]
        self.CustomReport = self.env["report.product_print_category.report_pricetag"]
        self.print_category = self.env.ref("product_print_category.demo_category")

    # Test Section
    def test_01_to_print_value(self):
        product = self.ProductProduct.create(
            {
                "name": "Demo Product Name",
            }
        )
        self.assertEqual(product.to_print, False)

        product.print_category_id = self.print_category.id
        self.assertEqual(product.to_print, True)

        product.to_print = False
        product.name = "Demo Product Name Changed"
        self.assertEqual(product.to_print, True)

    def test_10_test_wizard_obsolete(self):
        products = self.ProductProduct.search(
            [
                ("to_print", "=", True),
                ("print_category_id", "=", self.print_category.id),
            ]
        )
        wizard = self.ProductPrintWizard.with_context(
            active_model="product.print.category",
            active_ids=[self.print_category.id],
        ).create({})
        self.assertEqual(
            len(wizard.line_ids),
            len(products),
            "Print obsolete product should propose 1 product",
        )

    def test_11_test_wizard_all(self):
        products = self.ProductProduct.search(
            [
                ("print_category_id", "=", self.print_category.id),
            ]
        )
        wizard = self.ProductPrintWizard.with_context(
            active_model="product.print.category",
            active_ids=[self.print_category.id],
            all_products=True,
        ).create({})
        self.assertEqual(
            len(wizard.line_ids),
            len(products),
            "Print all products should propose 3 products",
        )
