# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale - Recurring Orders Duplication module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import orm, fields
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class SaleOrderDuplicationWizard(orm.TransientModel):
    _name = 'sale.order.duplication.wizard'

    _DUPLICATION_TYPE_KEYS = [
        ('week', 'Weekly'),
        ('month', 'Monthly'),
    ]

    # Column Section
    _columns = {
        'order_id': fields.many2one(
            'sale.order', string='Sale Order', readonly=True,
            required=True),
        'partner_id': fields.many2one(
            'res.partner', string='Customer', readonly=True),
        'begin_date': fields.date(
            string='Begin Date', required=True),
        'include_current_date': fields.boolean(
            string='Include Current Date'),
        'duplication_type': fields.selection(
            _DUPLICATION_TYPE_KEYS, string='Duplication Type', required=True),
        'duplication_duration': fields.integer(
            string='Duplication Duration', required=True),
        'line_ids': fields.one2many(
            'sale.order.duplication.wizard.line',
            'wizard_id', string='New Dates'),
    }

    # Default Section
    def _default_order_id(self, cr, uid, context=None):
        return context.get('active_id', False)

    def _default_begin_date(self, cr, uid, context=None):
        so_obj = self.pool['sale.order']
        so_id = context.get('active_id', False)
        if not so_id:
            return False
        else:
            return so_obj.browse(
                cr, uid, so_id, context=context).requested_date

    def _default_partner_id(self, cr, uid, context=None):
        so_obj = self.pool['sale.order']
        so_id = context.get('active_id', False)
        if not so_id:
            return False
        else:
            return so_obj.browse(cr, uid, so_id, context=context).partner_id.id

    _defaults = {
        'duplication_type': 'week',
        'duplication_duration': 0,
        'include_current_date': False,
        'order_id': _default_order_id,
        'begin_date': _default_begin_date,
        'partner_id': _default_partner_id,
    }

    # View Section
    def onchange_duplication_settings(
            self, cr, uid, ids, begin_date_str, duplication_type,
            duplication_duration, include_current_date, context=None):
        res = {'value': {'line_ids': []}}
        if (begin_date_str and duplication_type and duplication_duration):
            begin_date = datetime.datetime.strptime(begin_date_str, '%Y-%m-%d')
            for i in range(1, duplication_duration + 1):
                if include_current_date:
                    i -= 1
                if duplication_type == 'week':
                    current_date = begin_date + datetime.timedelta(weeks=i)
                elif duplication_type == 'month':
                    current_date = begin_date + relativedelta(months=i)
                else:
                    raise except_osv(
                        _("Unimplemented Feature!"),
                        _("The duplication type '%s' is not implemented") % (
                            duplication_type))
                res['value']['line_ids'].append((0, 0, {
                    'date': current_date.strftime('%Y-%m-%d'),
                }))
        return res

    def duplicate_button(self, cr, uid, ids, context=None):
        so_obj = self.pool['sale.order']
        for wizard in self.browse(cr, uid, ids, context=context):
            for line in wizard.line_ids:
                so_id = so_obj.copy(
                    cr, uid, wizard.order_id.id, context=context)
                so_obj.write(cr, uid, [so_id], {
                    'requested_date': line.date
                }, context=context)
        return True
