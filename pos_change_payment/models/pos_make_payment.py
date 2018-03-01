# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
from openerp import netsvc


class PosMakePayment(models.TransientModel):
    _inherit = 'pos.make.payment'

    @api.multi
    def check(self):
        """Check the order:
        if the order is not paid: continue payment,
        if the order is paid print ticket.
        """
        order_obj = self.env['pos.order']
        active_id = self._context.get('active_id', False)

        order = order_obj.browse(active_id)
        amount = order.amount_total - order.amount_paid
        data = self.read()[0]
        data['journal'] = int(data['journal_id'])

        if amount != 0.0:
            order.add_payment_v8(data)

        if order.test_paid():
            wf_service = netsvc.LocalService('workflow')
            wf_service.trg_validate(
                self._uid, 'pos.order', active_id, 'paid', self._cr)
            return {'type': 'ir.actions.act_window_close'}

        return self.launch_payment()

    # Selection Section
    @api.model
    def _select_journals(self):
        return self.env['account.journal']._get_pos_journal_selection()

    # Default Section
    @api.model
    def _default_journal(self):
        journal_obj = self.env['account.journal']
        res = journal_obj._get_pos_journal_selection()
        if res and len(res) > 1:
            return res[0][0]
        else:
            return False

    # Column Section
    # Overload journal_id from many2one to selection
    journal_id = fields.Selection(
        selection=_select_journals, default=_default_journal)
