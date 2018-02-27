# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class TestRecurringConsignment(TransactionCase):
    """Tests for 'Recurring Consignment' Module"""

    def setUp(self):
        super(TestRecurringConsignment, self).setUp()

        self.product_obj = self.env['product.product']
        self.sale_order = self.env.ref('recurring_consignment.sale_order_1')
        self.consigned_product_vat_5 = self.env.ref(
            'recurring_consignment.consigned_product_consignor_1_vat_5')
        self.consigned_product_vat_5_2 = self.env.ref(
            'recurring_consignment.consigned_product_consignor_1_vat_5_2')
        self.second_consignor = self.env.ref(
            'recurring_consignment.consignor_2')
        self.sale_pricelist = self.env.ref(
            'recurring_consignment.sale_pricelist')

    # Test Section
    def test_01_change_consignor_possible(self):
        """Test if it's possible to change a consignor for an unmoved
        Product."""
        self.consigned_product_vat_5_2.consignor_partner_id =\
            self.second_consignor.id

    def test_02_change_consignor_impossible_moved(self):
        """Test if it's possible to change a consignor for an moved
        Product."""
        self.sale_order.action_button_confirm()
        with self.assertRaises(UserError):
            self.consigned_product_vat_5_2.consignor_partner_id =\
                self.second_consignor.id

    def test_03_change_consignor_impossible_invoiced(self):
        """Test if it's possible to change a consignor for an invoiced
        Product."""
        with self.assertRaises(UserError):
            self.consigned_product_vat_5.consignor_partner_id =\
                self.second_consignor.id

    def test_04_pricelist_existing_product_active(self):
        """Test if pricelist mechanism works fine for existing products"""
        self.sale_pricelist.for_consigned_product = True
        self._test_pricelist(self.consigned_product_vat_5, True)

    def test_05_pricelist_existing_product(self):
        """Test if pricelist mechanism works fine for existing products"""
        self.sale_pricelist.for_consigned_product = False
        self._test_pricelist(self.consigned_product_vat_5, False)

    def test_06_pricelist_create_product_active(self):
        """Test if pricelist mechanism works fine for created products"""
        self.sale_pricelist.for_consigned_product = True
        product = self.product_obj.create({
            'name': 'New Product',
            'list_price': 100,
            'consignor_partner_id': self.second_consignor.id,
        })
        self._test_pricelist(product, True)

    def test_07_pricelist_create_product_inactive(self):
        """Test if pricelist mechanism works fine for created products"""
        self.sale_pricelist.for_consigned_product = False
        product = self.product_obj.create({
            'name': 'New Product',
            'list_price': 100,
            'consignor_partner_id': self.second_consignor.id,
        })
        self._test_pricelist(product, False)

    def _test_pricelist(self, product, active):
        list_price = product.list_price
        res = self.sale_pricelist.price_get(product.id, 1)
        if active:
            self.assertEqual(
                res[self.sale_pricelist.id], list_price / 2,
                "Pricelist should be applyed if pricelist"
                " 'for consigned product' is checked")
        else:
            res = self.sale_pricelist.price_get(product.id, 1)
            self.assertEqual(
                res[self.sale_pricelist.id], list_price,
                "Pricelist should not be applyed if pricelist"
                " 'for consigned product' is not checked")
