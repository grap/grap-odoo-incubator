# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model


class PosOrderLog(Model):
    _name = 'pos.order.log'
    _order = 'date desc, user_id'

    _columns = {
        'name': fields.char(string='Name'),
        'note': fields.text(string='Notes'),
        'user_id': fields.many2one('res.users', 'User', select=True),
        'date': fields.datetime(string='Date', select=True),
    }
