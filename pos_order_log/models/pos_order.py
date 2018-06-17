# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time

from openerp import api, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def _prepare_pos_order_log(self, order_data):
        return {
            'name': order_data['data']['name'],
            'amount_total': order_data['data']['amount_total'],
            'session_id': order_data['data']['pos_session_id'],
            'company_id': self.env.user.company_id.id,
            'note': order_data['data'],
            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.env.user.id,
        }

    @api.model
    def create_from_ui(self, orders):
        log_obj = self.env['pos.order.log']
        for order in orders:
            log_obj.create(self._prepare_pos_order_log(order))
        return super(PosOrder, self).create_from_ui(orders,)
