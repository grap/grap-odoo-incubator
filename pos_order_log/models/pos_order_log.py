# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class PosOrderLog(models.Model):
    _name = 'pos.order.log'
    _order = 'date desc'

    name = fields.Char(string='Name')

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', select=True)

    session_id = fields.Many2one(
        comodel_name='pos.session', string='Session', select=True)

    note = fields.Text(string='Notes')

    user_id = fields.Many2one('res.users', 'User', select=True)

    date = fields.Datetime(string='Date', select=True)

    amount_total = fields.Float(string='Total')
