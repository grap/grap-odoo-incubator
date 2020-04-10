# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, exceptions, fields, _
from odoo.addons.point_of_sale.wizard.pos_box import PosBox


class PosBoxJournalReason(PosBox):
    _register = False

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        domain="[('journal_user', '=', True)]",
    )

    statement_id = fields.Many2one(
        comodel_name="account.bank.statement",
        string="Statement",
        compute="_compute_statement_id",
    )

    @api.depends("journal_id")
    def _compute_statement_id(self):
        active_model = self.env.context.get("active_model", False) or False
        active_id = self.env.context.get("active_id", False) or False

        session = self.env[active_model].browse(active_id)
        if session:
            for cashbox in self:
                for statement in session.statement_ids:
                    if statement.journal_id.id == cashbox.journal_id.id:
                        cashbox.statement_id = statement.id

    @api.model
    def _create_bank_statement_line(self, box, record):
        """Overwrite Section to allow to write in any statement, and not
        only the cash statement"""
        statement_obj = self.env["account.bank.statement"]
        values = self._compute_values_for_statement_line(box, record)
        # wizard : native cash.box.out/in
        # not wizard : quick autosolve
        if self.env.context.get("wizard", True):
            values.update(
                {
                    "journal_id": box.journal_id.id,
                    "statement_id": box.statement_id.id,
                }
            )
        statement = statement_obj.browse(values["statement_id"])
        if statement.state == "confirm":
            raise exceptions.Warning(
                _(
                    "You cannot put/take money in/out for the statement"
                    " %s which is closed"
                )
                % statement.name
            )
        return statement.write({"line_ids": [(0, False, values)]})


class PosBoxIn(PosBoxJournalReason):
    _inherit = "cash.box.in"


class PosBoxOut(PosBoxJournalReason):
    _inherit = "cash.box.out"

    ref = fields.Char(string="Reference")

    def _compute_values_for_statement_line(self, box, record):
        values = super(PosBoxOut, self)._compute_values_for_statement_line(
            box, record
        )
        values["ref"] = box.ref or ""
        return values
