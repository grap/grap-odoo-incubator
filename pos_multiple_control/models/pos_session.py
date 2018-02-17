# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class PosSession(models.Model):
    _inherit = 'pos.session'

    # Columns Section
    statement_ids = fields.One2many(readonly=False)

    control_statement_ids = fields.One2many(
        string='Statements', comodel_name='account.bank.statement',
        related='statement_ids')

    summary_statement_ids = fields.One2many(
        string='Statements', comodel_name='account.bank.statement',
        related='statement_ids')

    control_register_balance_start = fields.Float(
        compute='_compute_control_register_balance_start',
        string='Opening Balances')

    control_register_total_entry_encoding = fields.Float(
        compute='_compute_control_register_total_entry_encoding',
        string='Transactions')

    control_register_balance_end = fields.Float(
        compute='_compute_control_register_balance_end',
        string='Theoretical Closing Balances')

    control_register_balance = fields.Float(
        compute='_compute_control_register_balance',
        string='Real Closing Balances')

    control_register_difference = fields.Float(
        compute='_compute_control_register_difference',
        string='Differences')

    # Compute Section
    @api.multi
    @api.depends('statement_ids.is_pos_control', 'statement_ids.balance_start')
    def _compute_control_register_balance_start(self):
        for session in self:
            session.control_register_balance_start = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control).mapped('balance_start'))

    @api.multi
    @api.depends(
        'statement_ids.is_pos_control', 'statement_ids.total_entry_encoding')
    def _compute_control_register_total_entry_encoding(self):
        for session in self:
            session.control_register_total_entry_encoding = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control).mapped('total_entry_encoding'))

    @api.multi
    @api.depends(
        'statement_ids.is_pos_control', 'statement_ids.balance_end')
    def _compute_control_register_balance_end(self):
        for session in self:
            session.control_register_balance_end = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control).mapped('balance_end'))

    @api.multi
    @api.depends(
        'statement_ids.is_pos_control', 'statement_ids.control_balance')
    def _compute_control_register_balance(self):
        for session in self:
            session.control_register_balance = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control).mapped('control_balance'))

    @api.multi
    @api.depends(
        'statement_ids.is_pos_control', 'statement_ids.control_difference')
    def _compute_control_register_difference(self):
        for session in self:
            session.control_register_difference = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control).mapped('control_difference'))

    # Overload Section
    @api.model
    def create(self, vals):
        session = super(PosSession, self).create(vals)
        session.opening_details_ids.write({'is_piece': True})
        return session

    @api.multi
    def wkf_action_closing_control(self):
        for session in self:
            draft_orders = session.order_ids.filtered(
                lambda x: x.state == 'draft')
            if len(draft_orders):
                raise UserError(_(
                    "You can not end this session because there are some"
                    " draft orders: \n\n- %s") % (
                        '\n- '.join([x.name for x in draft_orders])))
        return super(PosSession, self).wkf_action_closing_control()

    @api.multi
    def wkf_action_close(self):
        for session in self:
            for statement in session.statement_ids:
                if statement.control_difference > 0.00001:
                    raise UserError(_(
                        "You can not close this session because the statement"
                        " %s has a not null difference: \n\n%f") % (
                            statement.name, statement.control_difference))
        return super(PosSession, self).wkf_action_close()

    @api.multi
    def _check_unicity(self):
        for session in self:
            domain = [
                ('state', 'in', ['opening_control', 'opened']),
                ('user_id', '=', session.user_id.id)
            ]
            if self.search_count(domain) > 1:
                return False
        return True

    @api.multi
    def _check_pos_config(self):
        for session in self:
            domain = [
                ('state', 'in', ['opening_control', 'opened']),
                ('config_id', '=', session.config_id.id)
            ]
            if self.search_count(domain) > 1:
                return False
        return True

    _constraints = [
        (
            _check_unicity, "You cannot create two active sessions with the"
            " same responsible!", ['user_id', 'state']),
        (
            _check_pos_config, "You cannot create two active sessions related"
            " to the same point of sale!", ['config_id', 'state']),
    ]
