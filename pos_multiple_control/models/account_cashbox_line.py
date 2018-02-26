# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountCashboxLine(models.Model):
    _inherit = 'account.cashbox.line'

    # Columns Section
    is_piece = fields.Boolean(string='Is Piece', readonly=True)
