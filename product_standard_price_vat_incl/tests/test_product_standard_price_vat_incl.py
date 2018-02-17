# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductStandardPriceVatIncluded(TransactionCase):
    """Tests for 'Product Standard Price VAT Included' Module"""

    def setUp(self):
        super(TestProductStandardPriceVatIncluded, self).setUp()

        self.pricelist = self.env.ref(
            'product_standard_price_vat_incl.pricelist')
        self.template = self.env.ref(
            'product_standard_price_vat_incl.product_template')

    # Test Section
    def test_01_correct_vat_compute(self):
        """Test if the total of a sale order is correct with price
        based on Price List VAT Included."""

        price_vat_incl = self.pricelist.price_get(
            self.template.product_variant_ids[0].id, 1)[self.pricelist.id]

        self.assertEquals(
            price_vat_incl, 11.5,
            """Computation of Price based on Cost VAT Included incorrect.""")
