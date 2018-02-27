# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Recurring Invoices Duplication module for Odoo
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


class AccountInvoiceDuplicationWizard(orm.TransientModel):
    _name = 'account.invoice.duplication.wizard'

    _DUPLICATION_TYPE_KEYS = [
        ('week', 'Weekly'),
        ('month', 'Monthly'),
    ]

    # Column Section
    _columns = {
        'invoice_id': fields.many2one(
            'account.invoice', string='Invoice', readonly=True,
            required=True),
        'partner_id': fields.many2one(
            'res.partner', string='Partner', readonly=True),
        'begin_date': fields.date(
            string='Begin Date', required=True),
        'include_current_date': fields.boolean(
            string='Include Current Date'),
        'duplication_type': fields.selection(
            _DUPLICATION_TYPE_KEYS, string='Duplication Type', required=True),
        'duplication_duration': fields.integer(
            string='Duplication Duration', required=True),
        'line_ids': fields.one2many(
            'account.invoice.duplication.wizard.line',
            'wizard_id', string='New Dates'),
        'date_due_duration': fields.integer(
            'Due Date Duration', required=True),
    }

    # Default Section
    def _default_invoice_id(self, cr, uid, context=None):
        return context.get('active_id', False)

    def _default_date_due_duration_id(self, cr, uid, context=None):
        ai_obj = self.pool['account.invoice']
        ai_id = context.get('active_id', False)
        if not ai_id:
            return 0
        else:
            ai = ai_obj.browse(cr, uid, ai_id, context=context)
            if not ai.date_due or not ai.date_invoice:
                return 0
            else:
                date_invoice =\
                    datetime.datetime.strptime(ai.date_invoice, '%Y-%m-%d')
                due_date = datetime.datetime.strptime(ai.date_due, '%Y-%m-%d')
                return (due_date - date_invoice).days

    def _default_begin_date(self, cr, uid, context=None):
        ai_obj = self.pool['account.invoice']
        ai_id = context.get('active_id', False)
        if not ai_id:
            return False
        else:
            return ai_obj.browse(
                cr, uid, ai_id, context=context).date_invoice

    def _default_partner_id(self, cr, uid, context=None):
        ai_obj = self.pool['account.invoice']
        ai_id = context.get('active_id', False)
        if not ai_id:
            return False
        else:
            return ai_obj.browse(cr, uid, ai_id, context=context).partner_id.id

    _defaults = {
        'duplication_type': 'month',
        'duplication_duration': 0,
        'include_current_date': False,
        'invoice_id': _default_invoice_id,
        'begin_date': _default_begin_date,
        'partner_id': _default_partner_id,
        'date_due_duration': _default_date_due_duration_id,
    }

    # View Section
    def onchange_duplication_settings(
            self, cr, uid, ids, begin_date_str, duplication_type,
            duplication_duration, include_current_date, date_due_duration,
            context=None):
        res = {'value': {'line_ids': []}}
        if (begin_date_str and duplication_type and duplication_duration):
            begin_date = datetime.datetime.strptime(begin_date_str, '%Y-%m-%d')
            for i in range(1, duplication_duration + 1):
                if include_current_date:
                    i -= 1
                if duplication_type == 'week':
                    date_invoice = begin_date + datetime.timedelta(weeks=i)
                elif duplication_type == 'month':
                    date_invoice = begin_date + relativedelta(months=i)
                else:
                    raise except_osv(
                        _("Unimplemented Feature!"),
                        _("The duplication type '%s' is not implemented") % (
                            duplication_type))
                date_due =\
                    date_invoice + datetime.timedelta(days=date_due_duration)
                res['value']['line_ids'].append((0, 0, {
                    'date_invoice': date_invoice.strftime('%Y-%m-%d'),
                    'date_due': date_due.strftime('%Y-%m-%d'),
                }))
        return res

    def duplicate_button(self, cr, uid, ids, context=None):
        ai_obj = self.pool['account.invoice']
        for wizard in self.browse(cr, uid, ids, context=context):
            for line in wizard.line_ids:
                ai_id = ai_obj.copy(
                    cr, uid, wizard.invoice_id.id, context=context)
                ai_obj.write(cr, uid, [ai_id], {
                    'date_invoice': line.date_invoice,
                    'date_due': line.date_due,
                }, context=context)
        return True
