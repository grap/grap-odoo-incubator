# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestSimpleTaxAccount(TransactionCase):
    """Tests for 'Simple Tax - Account' Module"""

    def setUp(self):
        super(TestSimpleTaxAccount, self).setUp()
        self.invoice = self.env.ref('simple_tax_account.customer_invoice_1')
        self.vat_5_include = self.env.ref('simple_tax_account.vat_5_include')
        self.vat_5_exclude = self.env.ref('simple_tax_account.vat_5_exclude')

        self.template_include = self.env.ref(
            'simple_tax_account.template_vat_incl')
        self.template_exclude = self.env.ref('account.itaxs')

        self.partner_tax_included = self.env.ref(
            'simple_tax_account.partner_tax_included')
        self.partner_tax_excluded = self.env.ref(
            'simple_tax_account.partner_tax_excluded')
        self.invoice_line_tax_incl = self.env.ref(
            'simple_tax_account.customer_invoice_1_line_1')
        self.invoice_line_tax_excl = self.env.ref(
            'simple_tax_account.customer_invoice_1_line_2')
        self.amount_untaxed = self.invoice.amount_untaxed
        self.amount_total = self.invoice.amount_total

    def test_01_setting_none(self):
        self.invoice.recompute_simple_tax()
        self.invoice.button_reset_taxes()
        self._check_tax_line(self.invoice_line_tax_incl, self.vat_5_include)
        self._check_tax_line(self.invoice_line_tax_excl, self.vat_5_exclude)
        self._check_amount_unchanged(self.invoice)

    def test_02_setting_incl(self):
        self.invoice.partner_id = self.partner_tax_included.id
        self.invoice.recompute_simple_tax()
        self.invoice.button_reset_taxes()
        self._check_tax_line(self.invoice_line_tax_incl, self.vat_5_include)
        self._check_tax_line(self.invoice_line_tax_excl, self.vat_5_include)
        self._check_amount_unchanged(self.invoice)

    def test_03_setting_excl(self):
        self.invoice.partner_id = self.partner_tax_excluded.id
        self.invoice.recompute_simple_tax()
        self.invoice.button_reset_taxes()
        self._check_tax_line(self.invoice_line_tax_incl, self.vat_5_exclude)
        self._check_tax_line(self.invoice_line_tax_excl, self.vat_5_exclude)
        self._check_amount_unchanged(self.invoice)

    def _check_tax_line(self, line, tax):
        self.assertEqual(
            len(line.invoice_line_tax_id), 1,
            "Incorrect quantity of taxes on the invoice line.")
        self.assertEqual(
            line.invoice_line_tax_id[0].id, tax.id,
            "Incorrect tax on the invoice line.")

    def _check_amount_unchanged(self, invoice):
        self.assertEqual(
            invoice.amount_untaxed, self.amount_untaxed,
            "Total amount Untaxed changed.")
        self.assertEqual(
            invoice.amount_total, self.amount_total,
            "Total amount changed.")

    def test_06_tax_propagation(self):
        self.vat_5_include.simple_tax_id = False
        self.assertEqual(
            self.vat_5_exclude.simple_tax_id.id, False,
            "Removing related simple tax to a tax should remove it to the"
            " according related tax.")

        self.vat_5_include.simple_tax_id = self.vat_5_exclude
        self.assertEqual(
            self.vat_5_exclude.simple_tax_id, self.vat_5_include,
            "Set a related simple tax to a tax should add it to the"
            " according related tax.")

    def test_06_template_propagation(self):
        self.template_include.simple_template_id = False
        self.assertEqual(
            self.template_exclude.simple_template_id.id, False,
            "Removing related simple template to a teamplate should remove it"
            " to the according related template.")

        self.template_include.simple_template_id = self.template_exclude
        self.assertEqual(
            self.template_exclude.simple_template_id, self.template_include,
            "Set a related simple template to a template should add it to the"
            " according related template.")
