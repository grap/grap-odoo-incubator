# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestSaleOrderMassAction(TransactionCase):
    """Tests for 'Sale Order - Mass Action' Module"""

    def setUp(self):
        super(TestSaleOrderMassAction, self).setUp()
        self.wizard_obj = self.env['sale.order.mass.action.wizard']
        self.order_2 = self.env.ref('sale.sale_order_2')
        self.order_3 = self.env.ref('sale.sale_order_3')

    # Test Section
    def test_02_mass_confirmation(self):
        wizard = self.wizard_obj.with_context(active_ids=[
            self.order_2.id, self.order_3.id
        ]).create({
            'finish': False,
        })
        wizard.apply_button()
        self.assertEqual(
            self.order_2.state, 'manual',
            "Mass confirmation should set sale order 2 in 'To invoice' state")
        self.assertEqual(
            self.order_3.state, 'manual',
            "Mass confirmation should set sale order 2 in 'To invoice' state")
