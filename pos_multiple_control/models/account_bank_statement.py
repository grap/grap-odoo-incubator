# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError
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

    pos_session_state = fields.Char(
        string='Pos session state',
        compute='_compute_pos_session_state')

    display_autosolve = fields.Boolean(
        string='Control Difference',
        compute='_compute_display_autosolve')

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

    @api.multi
    def _compute_pos_session_state(self):
        for statement in self:
            statement.pos_session_state = statement.pos_session_id.state

    @api.multi
    def _compute_display_autosolve(self):
        for statement in self:
            if statement.pos_session_id.config_id.autosolve_limit:
                difference_with_limit =\
                    abs(statement.control_difference) -\
                    statement.pos_session_id.config_id.autosolve_limit
            else:
                difference_with_limit = -1
            # Display button autosolve with some conditions
            statement.display_autosolve =\
                (statement.pos_session_state in ['opened', 'closing_control']
                    and difference_with_limit < 0
                    and abs(round(statement.control_difference, 3)) != 0)

    @api.multi
    @api.depends('pos_session_state')
    def automatic_solve(self):
        for statement in self:
            product = statement.pos_session_id.config_id.autosolve_product
            if product:
                cb_product_id = product.id
                cb_difference = statement.control_difference
                cb_journal_id = statement.journal_id.id
                cb_ref = statement.pos_session_id.name
                if cb_difference < 0:
                    cashbox_type = 'cash.box.out'
                else:
                    cashbox_type = 'cash.box.in'
                _cashbox = statement.env[cashbox_type].create({
                    'name': _('Automatic solve'),
                    'amount': cb_difference,
                    'journal_id': cb_journal_id,
                    'product_id': cb_product_id,
                    'ref': cb_ref
                })
                # Parameter 'wizard' is used to not update info according to an
                # active cashbox that doesn't exist in this with_context
                _cashbox.with_context(wizard=False).\
                    _create_bank_statement_line(_cashbox, statement)
            else:
                raise UserError(_(
                    "We can't autosolve this difference. \nYou need to "
                    "configure the Point Of Sale Config and choose a "
                    "particular product for autosolving this difference."))
