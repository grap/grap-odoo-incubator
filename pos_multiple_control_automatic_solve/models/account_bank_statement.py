# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    pos_session_state = fields.Char(
        string='Pos session state',
        compute='_compute_pos_session_state')

    display_autosolve = fields.Boolean(
        string='Control Difference',
        compute='_compute_display_autosolve')

    # Compute Section
    @api.one
    def _compute_pos_session_state(self):
        self.pos_session_state = self.pos_session_id.state

    @api.one
    def _compute_display_autosolve(self):
        if self.pos_session_id.config_id.autosolve_limit:
            difference_with_limit =\
                abs(self.control_difference) -\
                self.pos_session_id.config_id.autosolve_limit
        else:
            difference_with_limit = -1
        # Display button autosolve with some conditions
        self.display_autosolve =\
            (self.pos_session_state in ['opened', 'closing_control']
                and difference_with_limit < 0
                and abs(round(self.control_difference, 3)) != 0)

    @api.one
    def automatic_solve(self):
        product = self.pos_session_id.config_id.autosolve_product
        if product:
            cb_product_id = product.id
            cb_difference = self.control_difference
            cb_journal_id = self.journal_id.id
            cb_ref = self.pos_session_id.name
            if cb_difference < 0:
                cashbox_type = 'cash.box.out'
            else:
                cashbox_type = 'cash.box.in'
            _cashbox = self.env[cashbox_type].create({
                'name': _('Automatic solve'),
                'amount': cb_difference,
                'journal_id': cb_journal_id,
                'product_id': cb_product_id,
                'ref': cb_ref
            })
            # Parameter 'no_wizard' is used to not update info according to an
            # active cashbox that doesn't exist in this context
            _cashbox._create_bank_statement_line(_cashbox, self, 'no_wizard')
        else:
            raise UserError(_(
                "We can't autosolve this difference. \nYou need to configure "
                "the Point Of Sale Config and choose a particular product "
                "for autosolving this difference."))
