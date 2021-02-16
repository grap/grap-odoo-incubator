# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestModule(TransactionCase):
    """Tests for 'product_default_code_res_company_code' Module"""

    def setUp(self):
        super().setUp()
        self.ProductProduct = self.env["product.product"]

    # Test Section
    def test_01_create_product(self):
        # First reinitialize the sequence, to make
        # test idempotent
        sequence = self.env["ir.sequence"].search(
            [
                ("code", "=", "product_product.default_code"),
                ("prefix", "=", "C1-"),
            ]
        )
        sequence.number_next_actual = 1
        product = self.ProductProduct.create({"name": "Product test 1"})
        self.assertEqual(
            product.default_code,
            "C1-000001",
            "Create a product should generate a default code",
        )

        product = self.ProductProduct.create({"name": "Product test 2"})
        self.assertEqual(
            product.default_code,
            "C1-000002",
            "Create another product should increment the sequence",
        )
