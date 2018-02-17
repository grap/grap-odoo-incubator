# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import ValidationError
from openerp.exceptions import Warning as UserError


class TestMultipleControl(TransactionCase):
    """Tests for 'Point of Sale - Multiple Control' Module"""

    def setUp(self):
        super(TestMultipleControl, self).setUp()
        self.session_obj = self.env['pos.session']
        self.order_obj = self.env['pos.order']
        self.user_demo = self.ref('base.user_demo')
        self.product = self.env('product.product_product_3')
        self.pos_config = self.env.ref(
            'pos_multiple_control.pos_config_control')

    # Test Section
    def test_01_two_opening_session(self):
        # I create new session
        session_01 = self.session_obj.create(
            {'config_id': self.pos_config.id})

        # I Try to create a new session
        with self.assertRaises(ValidationError):
            self.session_obj.create({'config_id': self.pos_config.id})

    def test_02_opening_and_opened_session(self):
        # I create new session and open it
        session_01 = self.session_obj.create(
            {'config_id': self.pos_config.id})
        session_01.open_cb()

        # I Try to create a new session
        with self.assertRaises(ValidationError):
            self.session_obj.create({'config_id': self.pos_config.id})

    def test_03_check_close_session_with_draft_order(self):
        # I create new session and open it
        session_01 = self.session_obj.create(
            {'config_id': self.pos_config.id})
        session_01.open_cb()
        order = self.order_obj.create({'session_id': session_01.id})

        # I Try to close the session
        with self.assertRaises(UserError):
            session_01.signal_workflow('cashbox_control')

    def test_04_check_bank_statement_control(self):
        # I create new session and open it
        session_01 = self.session_obj.create(
            {'config_id': self.pos_config.id})
        session_01.open_cb()
        order = self.order_obj.create({
            'session_id': session_01.id,
            'lines': [(6, 0, {
                'name': 'OL/0001',
                'product_id': self.product.id,
                'qty': 1.0,
                'price_unit': 1000,
            })],
        })

        # I Try to close the session
        with self.assertRaises(UserError):
            session_01.signal_workflow('cashbox_control')
