# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):
    """Tests for 'Mass Merging Content - Test' Module"""

    def setUp(self):
        super(TestModule, self).setUp()
        self.wizard_obj = self.env['mass.merging.content.wizard']
        self.merging_content = self.env.ref(
            'mass_merging_content_test.merging_invoice')
        self.invoice = self.env.ref(
            'mass_merging_content_test.invoice_to_merge')
        self.imac_product = self.env.ref('product.product_product_8')

    # Test Section
    def test_01_merge_wizard(self):
        wizard = self.wizard_obj.with_context(
            active_ids=[self.invoice.id],
            active_model='account.invoice',
            mass_operation_mixin_name='mass.merging.content',
            mass_operation_mixin_id=self.merging_content.id).create({})
        wizard.button_apply()

        self.assertEqual(
            len(self.invoice.invoice_line), 3,
            "Merging content of invoice with 4 lines including 2 similars"
            " lines should generate an invoice with 3 lines.")

        # Get Merged lines
        lines = self.invoice.invoice_line.filtered(
            lambda x: x.product_id == self.imac_product and x.price_unit == 50)

        self.assertEqual(
            len(lines), 1,
            "Merging similar lines should generate a unique single line")

        self.assertEqual(
            lines[0].quantity, 3,
            "Incorrect 'sum' computation when merging lines")

        self.assertEqual(
            lines[0].name, self.imac_product.name,
            "Incorrect 'related' computation when merging lines")
