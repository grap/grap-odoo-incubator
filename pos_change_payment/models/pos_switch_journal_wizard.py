# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.osv import except_osv
from openerp.osv.orm import TransientModel
from openerp.tools.translate import _


class pos_switch_journal_wizard(TransientModel):
    _name = 'pos.switch.journal.wizard'

    def _get_new_statement_id(self, cr, uid, context=None):
        absl_obj = self.pool['account.bank.statement.line']
        abs_obj = self.pool['account.bank.statement']

        if context.get('active_model', False) != 'account.bank.statement.line':
            return True
        absl = absl_obj.browse(
            cr, uid, context.get('active_id'), context=context)
        abs_ids = [
            x.id for x in absl.pos_statement_id.session_id.statement_ids]

        res = abs_obj.read(
            cr, uid, abs_ids, ['id', 'journal_id'], context=context)
        res = [(
            r['id'], r['journal_id'][1])
            for r in res if r['id'] != absl.statement_id.id]
        return res

    _columns = {
        'statement_line_id': fields.many2one(
            'account.bank.statement.line', 'Statement',
            required=True, readonly=True),
        'old_journal_id': fields.many2one(
            'account.journal', 'Old Journal', required=True, readonly=True),
        'amount': fields.float('Amount', readonly=True),
        'new_statement_id': fields.selection(
            _get_new_statement_id, 'New Journal', required=True),
    }

    def default_get(self, cr, uid, fields, context=None):
        absl_obj = self.pool['account.bank.statement.line']
        if context.get('active_model', False) != 'account.bank.statement.line':
            raise except_osv(_('Error!'), _('Incorrect Call!'))
        res = super(pos_switch_journal_wizard, self).default_get(
            cr, uid, fields, context=context)
        absl = absl_obj.browse(
            cr, uid, context.get('active_id'), context=context)
        res.update({'statement_line_id': absl.id})
        res.update({'old_journal_id': absl.journal_id.id})
        res.update({'amount': absl.amount})
        return res

    # Action section
    def button_switch_journal(self, cr, uid, ids, context=None):
        po_obj = self.pool['pos.order']
        absl_obj = self.pool['account.bank.statement.line']
        psjw = self.browse(cr, uid, ids[0], context=context)
        absl = absl_obj.browse(
            cr, uid, psjw.statement_line_id.id, context=context)
        if absl.pos_statement_id:
            po_obj._allow_change_payments(
                cr, uid, [absl.pos_statement_id.id], context=context)

        # TODO (FIXME) when upstream is fixed.
        # We do 2 write, one in the old statement, one in the new, with
        # 'amount' value each time to recompute all the functional fields
        # of the Account Bank Statements
        amount = absl.amount
        ctx = context.copy()
        ctx['change_pos_payment'] = True
        absl_obj.write(cr, uid, [absl.id], {
            'amount': 0,
        }, context=ctx)
        # Change statement of the statement line
        absl_obj.write(cr, uid, [absl.id], {
            'amount': amount,
            'statement_id': int(psjw.new_statement_id),
        }, context=ctx)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
