# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class TestPosCopyOrderOpenedSession(TransactionCase):
    """Tests for 'Point of Sale - Copy Order Openened Session' Module"""

    def setUp(self):
        super(TestPosCopyOrderOpenedSession, self).setUp()
        self.session_obj = self.env['pos.session']
        self.order_obj = self.env['pos.order']
        self.payment_obj = self.env['pos.make.payment']
        self.product = self.env.ref('product.product_product_3')
        self.pos_config = self.env.ref('point_of_sale.pos_config_main')
        self.cash_journal = self.env.ref('account.cash_journal')

    def _open_and_sale(self):
        # I create new session
        session = self.session_obj.create({'config_id': self.pos_config.id})
        order = self.order_obj.create({
            'session_id': session.id,
            'lines': [[0, False, {
                'name': 'OL/0001',
                'product_id': self.product.id,
                'qty': 1.0,
                'price_unit': 100,
            }]],
        })
        payment = self.payment_obj.create({
            'journal_id': self.cash_journal.id,
            'amount': 100,
        })
        payment.with_context(active_id=order.id).check()
        return session, order

    # Test Section
    def test_01_test_duplicated_opened(self):
        session, order = self._open_and_sale()
        # Should Succeed
        order.copy()

    def test_02_test_duplicated_closed(self):
        session, order = self._open_and_sale()
        # Close session
        session.signal_workflow('cashbox_control')
        session.signal_workflow('close')
        with self.assertRaises(UserError):
            # Should Fail
            order.copy()
