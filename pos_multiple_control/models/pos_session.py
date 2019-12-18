# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class PosSession(models.Model):
    _inherit = "pos.session"

    # Columns Section
    statement_ids = fields.One2many(readonly=False)

    control_statement_ids = fields.One2many(
        string="Control statements",
        comodel_name="account.bank.statement",
        related="statement_ids",
    )

    summary_statement_ids = fields.One2many(
        string="Summary statements",
        comodel_name="account.bank.statement",
        related="statement_ids",
    )

    control_register_balance_start = fields.Float(
        compute="_compute_control_register_balance_start",
        string="Opening Balances",
    )

    control_register_total_entry_encoding = fields.Float(
        compute="_compute_control_register_total_entry_encoding",
        string="Transactions",
    )

    control_register_balance_end = fields.Float(
        compute="_compute_control_register_balance_end",
        string="Theoretical Closing Balances",
    )

    control_register_balance = fields.Float(
        compute="_compute_control_register_balance",
        string="Real Closing Balances",
    )

    control_register_difference = fields.Float(
        compute="_compute_control_register_difference", string="Differences"
    )

    # Compute Section
    @api.multi
    @api.depends("statement_ids.is_pos_control", "statement_ids.balance_start")
    def _compute_control_register_balance_start(self):
        for session in self:
            session.control_register_balance_start = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control
                ).mapped("balance_start")
            )

    @api.multi
    @api.depends(
        "statement_ids.is_pos_control", "statement_ids.total_entry_encoding"
    )
    def _compute_control_register_total_entry_encoding(self):
        for session in self:
            session.control_register_total_entry_encoding = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control
                ).mapped("total_entry_encoding")
            )

    @api.multi
    @api.depends("statement_ids.is_pos_control", "statement_ids.balance_end")
    def _compute_control_register_balance_end(self):
        print("============> Compute control_register_difference")
        for session in self:
            session.control_register_balance_end = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control
                ).mapped("balance_end_real")
            )

    @api.multi
    @api.depends(
        "statement_ids.is_pos_control", "statement_ids.control_balance"
    )
    def _compute_control_register_balance(self):
        print("============> Compute _compute_control_register_balance")
        for session in self:
            session.control_register_balance = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control
                ).mapped("control_balance")
            )

    @api.multi
    @api.depends(
        "statement_ids.is_pos_control", "statement_ids.control_difference"
    )
    def _compute_control_register_difference(self):
        print("============> Compute control_register_difference")
        # import pdb; pdb.set_trace();
        for session in self:
            session.control_register_difference = sum(
                session.statement_ids.filtered(
                    lambda x: x.is_pos_control
                ).mapped("control_difference")
            )

    # Overload Section
    @api.model
    def create(self, vals):
        session = super(PosSession, self).create(vals)
        # session.opening_details_ids.write({"is_piece": True})
        return session

        # TODO CHANGER JIMAGINE, voir le truc originel
    @api.multi
    def wkf_action_closing_control(self):
        for session in self:
            draft_orders = session.order_ids.filtered(
                lambda x: x.state == "draft"
            )
            if len(draft_orders):
                raise UserError(
                    _(
                        "You can not end this session because there are some"
                        " draft orders: \n\n- %s"
                    )
                    % ("\n- ".join([x.name for x in draft_orders]))
                )
        return super(PosSession, self).wkf_action_closing_control()

    # @api.multi
    # def action_pos_session_closing_control(self):
    #     self._check_pos_session_balance()
    #     for session in self:
    #         session.write({'state': 'closing_control', 'stop_at': fields.Datetime.now()})
    #         if not session.config_id.cash_control:
    #             session.action_pos_session_close()

    # TODO : Checker que si pos_control=True
    # TODO : actuellement sur les lignes on agit sur une variable "difference" alors qu'il faudrait agir sur control_difference comme c'est checké ici-meêm
    @api.multi
    def action_pos_session_closing_control(self):
        print("============> action_pos_session_closing_control")
        for session in self:
            for statement in session.statement_ids:
                if statement.journal_id.pos_control is True:
                    if abs(statement.control_difference) > 0.001:
                        raise UserError(
                            _(
                                "You can not close this session because the journal %s "
                                "(statement %s) has a not null difference: %s%s"
                            )
                            % (statement.journal_id.name, statement.name, str(round(statement.control_difference,3)), statement.currency_id.symbol)
                        )
        return super(PosSession, self).action_pos_session_closing_control()

    @api.multi
    def _check_unicity(self):
        for session in self:
            domain = [
                ("state", "in", ["opening_control", "opened"]),
                ("user_id", "=", session.user_id.id),
            ]
            if self.search_count(domain) > 1:
                return False
        return True

    @api.multi
    def _check_pos_config(self):
        for session in self:
            domain = [
                ("state", "in", ["opening_control", "opened"]),
                ("config_id", "=", session.config_id.id),
            ]
            if self.search_count(domain) > 1:
                return False
        return True



    _constraints = [
        (
            _check_unicity,
            "You cannot create two active sessions with the"
            " same responsible!",
            ["user_id", "state"],
        ),
        (
            _check_pos_config,
            "You cannot create two active sessions related"
            " to the same point of sale!",
            ["config_id", "state"],
        ),
    ]
