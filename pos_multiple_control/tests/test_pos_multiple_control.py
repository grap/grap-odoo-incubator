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
        self.payment_obj = self.env['pos.make.payment']
        self.product = self.env.ref('product.product_product_3')
        self.pos_config = self.env.ref(
            'pos_multiple_control.pos_config_control')
        self.check_journal = self.env.ref(
            'pos_multiple_control.check_journal')
        self.cash_journal = self.env.ref(
            'pos_multiple_control.cash_journal')

    def _sale(self, session, price, journal):
        order = self.order_obj.create({
            'session_id': session.id,
            'lines': [[0, False, {
                'name': 'OL/0001',
                'product_id': self.product.id,
                'qty': 1.0,
                'price_unit': price,
            }]],
        })
        payment = self.payment_obj.create({
            'journal_id': journal.id,
            'amount': price,
        })
        payment.with_context(active_id=order.id).check()
        return order

    # Test Section
    def test_01_two_opening_session(self):
        # I create new session
        self.session_obj.create({'config_id': self.pos_config.id})

        # I Try to create a new session
        with self.assertRaises(ValidationError):
            self.session_obj.create({'config_id': self.pos_config.id})

    def test_02_opening_and_opened_session(self):
        # I create new session and open it
        session = self.session_obj.create({'config_id': self.pos_config.id})
        session.open_cb()

        # I Try to create a new session
        with self.assertRaises(ValidationError):
            self.session_obj.create({'config_id': self.pos_config.id})

    def test_03_check_close_session_with_draft_order(self):
        # I create new session and open it
        session = self.session_obj.create({'config_id': self.pos_config.id})
        session.open_cb()

        # Create a Draft order, and try to close the session
        self.order_obj.create({'session_id': session.id})
        with self.assertRaises(UserError):
            session.signal_workflow('cashbox_control')

    def test_04_check_bank_statement_control(self):
        # I create new session and open it
        session = self.session_obj.create({'config_id': self.pos_config.id})
        session.open_cb()
        self._sale(session, 1000, self.check_journal)
        session.signal_workflow('cashbox_control')
