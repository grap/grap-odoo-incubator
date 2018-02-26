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

        self.sale_order = self.env.ref('recurring_consignment.sale_order_1')
        self.consigned_product_vat_5 = self.env.ref(
            'recurring_consignment.consigned_product_consignor_1_vat_5')
        self.consigned_product_vat_5_2 = self.env.ref(
            'recurring_consignment.consigned_product_consignor_1_vat_5_2')
        self.second_consignor = self.env.ref(
            'recurring_consignment.consignor_2')

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
