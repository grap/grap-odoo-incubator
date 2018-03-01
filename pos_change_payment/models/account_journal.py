# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class account_journal(models.Model):
    _inherit = 'account.journal'

    # Private Function Section
    @api.model
    def _get_pos_journal_selection(self):
        """Return Account Journal available for payment in PoS Module"""
        session_obj = self.env['pos.session']

        if not self._context.get('pos_session_id', False):
            return []

        # Get Session of the Current PoS
        session = session_obj.browse(int(self._context.get('pos_session_id')))

        # Get Journals, order by type (cash before), and name
        cash_journals = self.search(
            [('id', 'in', session.journal_ids.ids), ('type', '=', 'cash')],
            order='name')
        res = [(j.id, j.name) for j in cash_journals]

        other_journals = self.search(
            [('id', 'in', session.journal_ids.ids), ('type', '!=', 'cash')],
            order='name')
        res += [(j.id, j.name) for j in other_journals]

        return res
