# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.product_obj = self.env['product.product']
        self.main_company = self.env.ref('base.main_company')

    # Test Section
    def _create_product(self, ean13, company_id):
        return self.product_obj.create({
            'name': 'Test',
            'ean13': ean13,
            'company_id': company_id,
            'categ_id': self.env.ref('product.product_category_all').id
        })

    def test_01_create_duplicate(self):
        """constrains of unicity for ean13 and company_id"""
        # Create a first product with an ean13, shoud work
        product = self._create_product('3760138839329', self.main_company.id)

        # Create another product with the same ean13, in another company
        # should work
        self._create_product('3760138839329', False)

        # Create again, with the same ean13, should fail
        with self.assertRaises(ValidationError):
            self._create_product('3760138839329', self.main_company.id)

        # Create again, with the same ean13, should fail even if original
        # product is disabled
        product.active = False
        with self.assertRaises(ValidationError):
            self._create_product('3760138839329', self.main_company.id)

    def test_02_copy_product(self):
        """Copy product should not copy ean13 field."""
        # Create a first product with an ean13, shoud work
        product = self._create_product('3760138839329', self.main_company.id)
        new_product = product.copy()
        self.assertEqual(
            new_product.ean13, False,
            "Copy a product should set the ean13 field to false")

    def test_03_duplicate_view(self):
        """Check if existing duplicates are correctly displayed"""
        # Create two products
        product1 = self._create_product(False, self.main_company.id)
        product2 = self._create_product(False, self.main_company.id)
        sql_req = """
            UPDATE product_product
            SET ean13 = %s where id in %s
        """
        args = ('3760138839329', (product1.id, product2.id),)
        self.env.cr.execute(sql_req, args)  # pylint: disable=invalid-commit
        res = self.product_obj.search([('ean_duplicates_exist', '=', True)])

        self.assertEqual(
            len(res), 2,
            "Incorrect result of the function _search_ean_duplicates_exist")
