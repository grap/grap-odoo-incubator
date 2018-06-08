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
        self.product_obj.create({
            'name': 'Test',
            'ean13': ean13,
            'company_id': company_id,
            'categ_id': self.env.ref('product.product_category_all').id
        })

    def test_01_copy_product(self):
        """check the constrains of unicity for ean13 and company_id"""
        # Create a first product with an ean13, shoud work
        self._create_product('3760138839329', self.main_company.id)

        # Create another product with the same ean13, in another company
        # should work
        self._create_product('3760138839329', False)

        # Create again, with the same ean13, should fail
        with self.assertRaises(ValidationError):
            self._create_product('3760138839329', self.main_company.id)
