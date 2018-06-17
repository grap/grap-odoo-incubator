# coding: utf-8
# Copyright (C) 2017: Opener B.V. (https://opener.amsterdam)
# @author: Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestModule(TransactionCase):

    def test_pos_order_log(self):
        product = self.env.ref('product.product_product_24')

        config = self.env.ref('point_of_sale.pos_config_main').copy()
        session = self.env['pos.session'].create({
            'user_id': self.env.user.id,
            'config_id': config.id})
        session.signal_workflow('open')
        self.env['pos.order'].create_from_ui([{
            'to_invoice': False,
            'data': {
                'user_id': self.env.user.id,
                'name': 'Order 00017-002-0003',
                'amount_paid': 12,
                'pos_session_id': session.id,
                'lines': [[0, 0, {
                    'product_id': product.id,
                    'price_unit': 6,
                    'name': product.name,
                    'discount': 0,
                    'qty': 2,
                    'tax_ids': [[6, False, []]],
                }]],
                'statement_ids': [[0, 0, {
                    'journal_id': False,
                    'amount': 12,
                    'name': '2017-07-20 13:08:37',
                    'account_id': config.journal_ids[
                        0].default_debit_account_id.id,
                    'statement_id': session.statement_ids[0].id,
                }]],
                'amount_tax': 0,
                'uid': '00017-002-0003',
                'amount_return': 0,
                'sequence_number': 3,
                'amount_total': 12,
            },
            'id': '00017-002-0003',
        }])
        pos_order = self.env['pos.order.log'].search(
            [('name', '=', 'Order 00017-002-0003')])
        self.assertTrue(pos_order)
