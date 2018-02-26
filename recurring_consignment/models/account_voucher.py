# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class AccountVoucher(Model):
    _inherit = 'account.voucher'

#    # Override section
#    def recompute_voucher_lines(
#            self, cr, uid, ids, partner_id, journal_id, price, currency_id,
#            ttype, date, context=None):
#        partner_obj = self.pool['res.partner']
#        move_line_obj = self.pool['account.move.line']
#        ctx = context.copy()
#        if partner_id:
#            partner = partner_obj.browse(cr, uid, partner_id, context=context)
#            if partner.is_consignor:
# #                ctx.update({
# #                    'partner_id': False,
# #                    'account_id': partner.consignment_account_id.id,
# #                })
#                move_line_ids = move_line_obj.search(
#                    cr, uid, [('state','=','valid'),
#                    ('account_id', '=', partner.consignment_account_id.id),
#                    ('reconcile_id', '=', False)], context=context)
#                ctx.update({
#                    'move_line_ids': move_line_ids,
#                })

#        res = super(AccountVoucher, self).recompute_voucher_lines(
#            cr, uid, ids, partner_id, journal_id, price, currency_id, ttype,
#            date, context=ctx)
#        print "**********>"
#        print "partner_id : %s" % partner_id
#        print "journal_id : %s" % journal_id
#        print "price : %s" % price
#        print "currency_id : %s" % currency_id
#        print "ttype %s" % ttype
#        print res
#        return res
