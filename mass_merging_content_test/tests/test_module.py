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

    # Test Section
    def test_01_merge_wizard(self):
        wizard = self.wizard_obj.with_context(
            active_ids=[self.invoice.id],
            active_mode='account.invoice',
            mass_operation_mixin_name='mass.merging.content',
            mass_operation_mixin_id=self.merging_content.id).create({})
        wizard.button_apply()

        # self.assertEqual(
        #     invoice_qty + 10, new_invoice_qty,
        #     "Duplication wizard should create new account invoices")
