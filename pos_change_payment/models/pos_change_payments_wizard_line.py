# -*- coding: utf-8 -*-
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class pos_change_payments_wizard_line(models.TransientModel):
    _name = 'pos.change.payments.wizard.line'

    wizard_id = fields.Many2one(
        comodel_name='pos.change.payments.wizard', ondelete='cascade')
    bank_statement_id = fields.Many2one(
        comodel_name='account.bank.statement', string='Journal')
    amount = fields.Float(string='Amount')
