# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model
import time


class PosOrder(Model):
    _inherit = 'pos.order'

    def create_from_ui(self, cr, uid, orders, context=None):
        log_obj = self.pool['pos.order.log']
        for order in orders:
            log_obj.create(cr, uid, {
                'name': order['data']['name'],
                'note': order['data'],
                'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': uid,
            }, context=context)

        res = super(PosOrder, self).create_from_ui(
            cr, uid, orders, context=context)
        return res
