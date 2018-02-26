# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestRecurringConsignment(TransactionCase):
    """Tests for 'Recurring Consignment' Module"""

    def setUp(self):
        super(TestRecurringConsignment, self).setUp()

#        self.pricelist = self.env.ref(
#            'product_standard_price_vat_incl.pricelist')
#        self.template = self.env.ref(
#            'product_standard_price_vat_incl.product_template')
        self.consigned_product_vat_5 = self.env.ref(
            'recurring_consignment.consigned_product_consignor_1_vat_5')
        self.second_consignor = self.env.ref(
            'recurring_consignment.consignor_2')

    # Test Section
    def test_01_change_consignor_possible(self):
        """Test if it's possible to change a consignor for an unmoved
        Product."""
        self.consigned_product_vat_5.consignor_id = self.second_consignor.id

#    def test_02_change_consignor_impossible(self):
#        """Test if it's possible to change a consignor for an unmoved
#        Product."""
#        self.consigned_product_vat_5.consignor_id = self.second_consignor.id


