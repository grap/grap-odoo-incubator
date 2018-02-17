# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    # Columns Section
    control_balance = fields.Float(
        string='Controled Balance',
        compute='_compute_control_balance',
        digits_compute=dp.get_precision('Account'))

    control_difference = fields.Float(
        string='Control Difference',
        compute='_compute_control_difference',
        digits_compute=dp.get_precision('Account'))

    is_pos_control = fields.Boolean(
        compute='_compute_is_pos_control', store=True, string='PoS Control')

    # Compute Section
    @api.multi
    @api.depends('closing_details_ids.subtotal_closing')
    def _compute_control_balance(self):
        for statement in self:
            statement.control_balance = sum(
                statement.mapped('closing_details_ids.subtotal_closing'))

    @api.multi
    @api.depends('control_balance', 'total_entry_encoding')
    def _compute_control_difference(self):
        for statement in self:
            statement.control_difference =\
                - statement.balance_start\
                - statement.total_entry_encoding\
                + statement.control_balance

    @api.multi
    @api.depends('journal_id.cash_control', 'journal_id.bank_control')
    def _compute_is_pos_control(self):
        for statement in self:
            journal = statement.journal_id
            if journal.type == 'cash':
                statement.is_pos_control = journal.cash_control
            elif journal.type == 'bank':
                statement.is_pos_control = journal.bank_control
            else:
                statement.is_pos_control = False
