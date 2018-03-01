# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api
from openerp.osv.orm import Model
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class pos_order(Model):
    _inherit = 'pos.order'

    @api.multi
    def add_payment_v8(self, data):
        """Hack to call old api. TODO-V10 : remove me."""
        for order in self:
            self.pool['pos.order'].add_payment(
                self._cr, self._uid, order.id, data, context=self._context)

    def _merge_cash_payment(self, cr, uid, ids, context=None):
        absl_obj = self.pool['account.bank.statement.line']
        for po in self.browse(cr, uid, ids, context=context):
            absl_cash_ids = [
                x.id for x in po.statement_ids
                if x.statement_id.journal_id.type == 'cash']
            new_payments = {}
            for line in absl_obj.read(
                    cr, uid, absl_cash_ids,
                    ['statement_id', 'amount'],
                    context=context):
                if line['statement_id'][0] in new_payments.keys():
                    new_payments[line['statement_id'][0]] += line['amount']
                else:
                    new_payments[line['statement_id'][0]] = line['amount']

            # Delete all obsolete account bank statement line
            absl_obj.unlink(cr, uid, absl_cash_ids, context=context)

            # Create a new ones
            for k, v in new_payments.items():
                self.add_payment(cr, uid, po.id, {
                    'statement_id': k,
                    'amount': v
                    }, context=context)

    # Overload Section
    def action_paid(self, cr, uid, ids, context=None):
        """ Merge all cash statement line of the Order"""
        context = context or {}
        ctx = context.copy()
        ctx['change_pos_payment'] = True
        self._merge_cash_payment(cr, uid, ids, context=ctx)
        return super(pos_order, self).action_paid(
            cr, uid, ids, context=context)

    # Private Function Section
    def _allow_change_payments(
            self, cr, uid, ids, context=None):
        """Return True if the user can change the payment of a POS, depending
        of the state of the current session."""
        for po in self.browse(cr, uid, ids, context=context):
            if po.session_id.state == 'closed':
                raise except_osv(
                    _('Error!'),
                    _("""You can not change payments of the POS '%s' because"""
                        """ the associated session '%s' has been closed!""" % (
                            po.name, po.session_id.name)))
        return True
