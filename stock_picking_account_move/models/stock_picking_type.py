# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        help="Set the Accounting Journal used to generate Accounting Entries",
    )

    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Expense Account",
        help="Expense account of the Use picking_type. The generated"
        " Entries will belong the following lines:\n\n"
        " * Debit: This Expense Account"
        " * Credit: The Default Expense Account of the Product",
    )

    # Constrains Section
    @api.constrains("journal_id", "account_id")
    def _constrains_account_journal(self):
        for picking_type in self:
            if (picking_type.journal_id and not picking_type.account_id) or (
                not picking_type.journal_id and picking_type.account_id
            ):
                raise UserError(
                    _(
                        "Incorrect Accounting Settings.\n"
                        "Account and Journal should be set both or not set."
                    )
                )
