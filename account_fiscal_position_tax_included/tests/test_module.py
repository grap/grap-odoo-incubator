# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.AccountInvoiceLine = self.env['account.invoice.line']

        self.fiscal_position_20_excl_to_20_incl = self.env.ref(
            'account_fiscal_position_tax_included.'
            'fiscal_position_20_excl_to_20_incl')

        self.fiscal_position_20_incl_to_20_excl = self.env.ref(
            'account_fiscal_position_tax_included.'
            'fiscal_position_20_incl_to_20_excl')

        self.product_20_tax_incl = self.env.ref(
            'account_fiscal_position_tax_included.product_20_tax_incl')

        self.product_20_tax_excl = self.env.ref(
            'account_fiscal_position_tax_included.product_20_tax_excl')

        self.uom = self.env.ref('product.product_uom_unit')
        self.partner = self.env.ref('base.res_partner_2')

    # Test Section
    def test_01_mapping_20_incl_to_20_excl(self):
        # 120 Tax Incl --> 100 Tax Excl
        self.product_20_tax_incl.lst_price = 120
        res = self.AccountInvoiceLine.product_id_change(
            self.product_20_tax_incl.id, self.uom.id, qty=1,
            partner_id=self.partner.id,
            fposition_id=self.fiscal_position_20_incl_to_20_excl.id)

        self.assertEqual(
            res['value']['price_unit'], 100)

        # 100 Tax Excl --> 100 Tax Excl
        self.product_20_tax_excl.lst_price = 100
        res = self.AccountInvoiceLine.product_id_change(
            self.product_20_tax_excl.id, self.uom.id, qty=1,
            partner_id=self.partner.id,
            fposition_id=self.fiscal_position_20_incl_to_20_excl.id)

        self.assertEqual(
            res['value']['price_unit'], 100)

    def test_02_mapping_20_excl_to_20_incl(self):
        # 100 Tax Excl -> 120 Tax Incl
        self.product_20_tax_excl.lst_price = 100
        res = self.AccountInvoiceLine.product_id_change(
            self.product_20_tax_excl.id, self.uom.id, qty=1,
            partner_id=self.partner.id,
            fposition_id=self.fiscal_position_20_excl_to_20_incl.id)

        self.assertEqual(
            res['value']['price_unit'], 120)

        # 100 Tax Incl -> 100 Tax Incl
        self.product_20_tax_incl.lst_price = 100
        res = self.AccountInvoiceLine.product_id_change(
            self.product_20_tax_incl.id, self.uom.id, qty=1,
            partner_id=self.partner.id,
            fposition_id=self.fiscal_position_20_excl_to_20_incl.id)

        self.assertEqual(
            res['value']['price_unit'], 100)
