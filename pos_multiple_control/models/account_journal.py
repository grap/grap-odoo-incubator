# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    bank_control = fields.Boolean(
        string='Bank and Checks Control', help="If you want this journal"
        " should be control at opening/closing, check this option")

    @api.onchange('type')
    def onchange_type(self):
        for journal in self:
            if journal.type == 'cash':
                journal.cash_control = True
            elif journal.type == 'bank':
                journal.bank_control = True
