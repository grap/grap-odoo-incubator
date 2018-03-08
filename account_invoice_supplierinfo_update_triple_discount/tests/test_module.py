# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.wizard_obj = self.env['wizard.update.invoice.supplierinfo']
        self.supplierinfo_obj = self.env['product.supplierinfo']
        self.partnerinfo_obj = self.env['pricelist.partnerinfo']
        self.invoice = self.env.ref('account.demo_invoice_0')
        self.invoice_line = self.env.ref(
            'account.demo_invoice_0_line_rpanrearpanelshe0')
        self.toner_template = self.env.ref(
            'product.product_product_39_product_template')

    # Test Section
    def test_01_triple_discount(self):
        # Set discounts on account lines
        self.invoice_line.write({
            'discount': 10.0,
            'discount2': 20.0,
            'discount3': 30.0,
        })

        # Launch and confirm Wizard
        lines_for_update = self.invoice._get_update_supplierinfo_lines()
        wizard = self.wizard_obj.with_context(
            default_line_ids=lines_for_update,
            default_invoice_id=self.invoice.id).create({})
        wizard.update_supplierinfo()

        # Check Regressions
        supplierinfo = self.supplierinfo_obj.search([
            ('product_tmpl_id', '=', self.toner_template.id),
            ('name', '=', self.invoice.partner_id.id)])

        self.assertEqual(
            len(supplierinfo), 1,
            "Regression : Confirming wizard should have create a supplierinfo")
        partnerinfo = self.partnerinfo_obj.search([
            ('suppinfo_id', '=', supplierinfo.id)])
        self.assertEqual(
            len(partnerinfo), 1,
            "Regression : Confirming wizard should have create a partnerinfo")
        self.assertEqual(
            partnerinfo.discount, 10,
            "Regression : Confirming wizard should have update main discount")

        # Check Correct Discounts
        self.assertEqual(
            partnerinfo.discount2, 20,
            "Confirming wizard should have update discount #2")
        self.assertEqual(
            partnerinfo.discount3, 30,
            "Confirming wizard should have update discount #3")
