# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestSimpleTaxSale(TransactionCase):
    """Tests for 'Simple Tax - Sale' Module"""

    def setUp(self):
        super(TestSimpleTaxSale, self).setUp()
        self.order = self.env.ref('simple_tax_sale.sale_order_1')
        self.vat_5_include = self.env.ref('simple_tax_account.vat_5_include')
        self.vat_5_exclude = self.env.ref('simple_tax_account.vat_5_exclude')
        self.partner_tax_included = self.env.ref(
            'simple_tax_account.partner_tax_included')
        self.partner_tax_excluded = self.env.ref(
            'simple_tax_account.partner_tax_excluded')
        self.order_line_tax_incl = self.env.ref(
            'simple_tax_sale.sale_order_1_line_1')
        self.order_line_tax_excl = self.env.ref(
            'simple_tax_sale.sale_order_1_line_2')
        self.amount_untaxed = self.order.amount_untaxed
        self.amount_total = self.order.amount_total

    def test_01_setting_none(self):
        self.order.recompute_simple_tax()
        self._check_tax_line(self.order_line_tax_incl, self.vat_5_include)
        self._check_tax_line(self.order_line_tax_excl, self.vat_5_exclude)
        self._check_amount_unchanged(self.order)

    def test_02_setting_incl(self):
        self.order.partner_id = self.partner_tax_included.id
        self.order.recompute_simple_tax()
        self._check_tax_line(self.order_line_tax_incl, self.vat_5_include)
        self._check_tax_line(self.order_line_tax_excl, self.vat_5_include)
        self._check_amount_unchanged(self.order)

    def test_03_setting_excl(self):
        self.order.partner_id = self.partner_tax_excluded.id
        self.order.recompute_simple_tax()
        self._check_tax_line(self.order_line_tax_incl, self.vat_5_exclude)
        self._check_tax_line(self.order_line_tax_excl, self.vat_5_exclude)
        self._check_amount_unchanged(self.order)

    def _check_tax_line(self, line, tax):
        self.assertEqual(
            len(line.tax_id), 1,
            "Incorrect quantity of taxes on the sale line.")
        self.assertEqual(
            line.tax_id[0].id, tax.id,
            "Incorrect tax on the sale line.")

    def _check_amount_unchanged(self, order):
        self.assertEqual(
            order.amount_untaxed, self.amount_untaxed,
            "Total amount Untaxed changed.")
        self.assertEqual(
            order.amount_total, self.amount_total,
            "Total amount changed.")
