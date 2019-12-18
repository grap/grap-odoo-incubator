# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError
import odoo.addons.decimal_precision as dp


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    # Columns Section
    control_balance = fields.Float(
        string="Controled Balance",
        compute="_compute_control_balance",
        digits_compute=dp.get_precision("Account"),
    )

    control_difference = fields.Float(
        string="Control Difference",
        compute="_compute_control_difference",
        digits_compute=dp.get_precision("Account"),
    )

    is_pos_control = fields.Boolean(
        string="Pos control Bank statement",
        compute="_compute_is_pos_control", store=True, 
    )

    pos_session_state = fields.Char(
        string="Pos session state", compute="_compute_pos_session_state"
    )

    display_autosolve = fields.Boolean(
        string="Display autosolve", compute="_compute_display_autosolve"
    )

    # TODO : à qué ça sert ce champ ?
    # Compute Section
    @api.multi
    # @api.depends("line_ids.subtotal_closing")
    @api.depends("line_ids")
    def _compute_control_balance(self):
        print("============> Compute control balance")
        for statement in self:
            statement.control_balance = sum(
                statement.mapped("line_ids.amount")
            )

    # MODIF ICI
    @api.multi
    @api.depends("control_balance", "total_entry_encoding", "balance_end_real")
    def _compute_control_difference(self):
        print("============> Compute control difference")
        for statement in self:
            statement.control_difference = (
                + statement.balance_end_real
                - statement.balance_start
                - statement.total_entry_encoding
            )

    @api.multi
    @api.depends("journal_id.pos_control", "pos_session_state")
    def _compute_is_pos_control(self):
        for statement in self:
            print("============> Compute control difference")
            # import pdb; pdb.set_trace()
            if statement.pos_session_state in ["opened", "closing_control"]:
                journal = statement.journal_id
                statement.is_pos_control = journal.pos_control
            else:
                statement.is_pos_control = False

    @api.multi
    @api.depends("pos_session_id.state")
    def _compute_pos_session_state(self):
        for statement in self:
            statement.pos_session_state = statement.pos_session_id.state

    @api.multi
    def _compute_display_autosolve(self):
        for statement in self:
            if statement.pos_session_id.config_id.autosolve_limit:
                difference_with_limit = (
                    abs(statement.control_difference)
                    - statement.pos_session_id.config_id.autosolve_limit
                )
            else:
                difference_with_limit = -1
            # Display button autosolve with some conditions
            statement.display_autosolve = (
                statement.pos_session_state in ["opened", "closing_control"]
                and difference_with_limit < 0
                and abs(round(statement.control_difference, 3)) != 0
            )

    @api.multi
    @api.depends("pos_session_state")
    def automatic_solve(self):
        self.WizardReason = self.env['wizard.pos.move.reason']
        for statement in self:
            pos_move_reason = statement.pos_session_id.config_id.autosolve_product
            if pos_move_reason:
                cb_pos_move_reason_id = pos_move_reason.id
                cb_difference = statement.control_difference
                cb_journal_id = statement.journal_id.id
                cb_ref = statement.pos_session_id.name
                if cb_difference < 0:
                    default_move_type="expense"
                else:
                    default_move_type="income"

                wizard = self.WizardReason.with_context(
                    active_id=statement.pos_session_id.id,
                    default_move_type=default_move_type).create({
                        'move_reason_id': cb_pos_move_reason_id,
                        'journal_id': cb_journal_id,
                        'statement_id': statement.id,
                        'amount': abs(cb_difference),
                        'name': 'Automatic solve',
                    })
                wizard.apply()

                # _pos_move_reason = statement.env["pos.move.reason"].create(
                #    {
                #        "name": _("Automatic solve"),
                #        "amount": cb_difference,
                #        "journal_id": cb_journal_id,
                #        "product_id": cb_product_id,
                #        "ref": cb_ref,
                #    }
                #)
                # Parameter 'wizard' is used to not update info according to an
                # active pos_move_reason that doesn't exist in this with_context
                #_pos_move_reason.with_context(
                #    active_model="pos.session",
                #    active_ids=[statement.pos_session_id.id],
                #    wizard=False,
                #)._create_bank_statement_line(_pos_move_reason, statement)
            else:
                raise UserError(
                    _(
                        "We can't autosolve this difference. \nYou need to "
                        "configure the Point Of Sale Config and choose a "
                        "particular product for autosolving this difference."
                    )
                )

    # @api.multi
    # @api.depends("pos_session_state")
    # def open_pos_move_reason_balance(self):
    #     self.ensure_one()
    #     action = self.env.ref(
    #         "pos_multiple_control."
    #         "action_pos_update_bank_statement_balance")
    #     result = action.read()[0]
    #     return result

    # @api.multi
    # @api.depends("pos_session_state")
    # def open_pos_move_reason_balance(self):
    #     import pdb; pdb.set_trace();
    #     self.ensure_one()
    #     cb_journal_id = self.journal_id.id
    #     # Créer pos_move_reason en se basant sur celui de poss sessin
    #     # TODO
    #     _update_balance = self.env["pos.update.bank.statement.balance"].create(
    #         {
    #             "name": _("Update Balance"),
    #             "journal_id": cb_journal_id,
    #         }
    #     )
    #     print("============= avec contexte =============")
    #     # Parameter 'wizard' is used to not update info according to an
    #     # active pos_move_reason that doesn't exist in this with_context
    #     _update_balance.with_context(
    #         active_model="pos.session",
    #         active_ids=[self.pos_session_id.id],
    #         wizard=True,
    #     )
    #     print("============= après contexte =============")
    #     result = _update_balance.read()[0]
    #     return result


################
# s'inspirer du travail fait pour pos_cash_move_reason de Sylvain pour les wizards :
# voici le début
# et mixer avec ce qu'il y a au dessus


    def open_cashbox_starting_balance(self):
        return self.open_cashbox_balance('starting')

    def open_cashbox_ending_balance(self):
        return self.open_cashbox_balance('ending')

    def open_cashbox_balance(self, balance_moment):
        print("======== open cashbox =============")
        action = self.env.ref(
            'pos_multiple_control.action_wizard_pos_update_bank_statement_balance').read()[0]
        action['context'] = {'balance_moment': balance_moment,\
                         'active_id' : [self.id],\
                         'active_pos_id' : [self.pos_session_id.id],\
                         'active_model' : 'pos.session'}
        return action

