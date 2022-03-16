# Copyright (C) 2013-Today GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class InternalUseCase(models.Model):
    _name = "internal.use.case"
    _description = "Internal Use Cases"

    # Default Section
    def _default_company_id(self):
        return self.env.user.company_id

    # Columns Section
    name = fields.Char(string="Name", required=True)

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        index=True,
        default=_default_company_id,
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help="By unchecking the active field,"
        " you may hide an Use Case without deleting it.",
    )

    default_location_src_id = fields.Many2one(
        comodel_name="stock.location", string="Origin Location", required=True,
    )

    default_location_dest_id = fields.Many2one(
        comodel_name="stock.location", string="Destination Location", required=True
    )

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        help="Set the Accounting Journal used to generate Accounting Entries",
    )

    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Expense Account",
        help="Expense account of the Use Case. The generated"
        " Entries will belong the following lines:\n\n"
        " * Debit: This Expense Account"
        " * Credit: The Default Expense Account of the Product",
    )

    # Overload Section
    @api.multi
    def copy_data(self, default=None):
        default = default and default or {}
        default["name"] = _("%s (copy)") % self.name
        return super().copy_data(default)

    # Constrains Section
    @api.constrains("journal_id", "account_id")
    def _constrains_account_journal(self):
        for case in self:
            if (case.journal_id and not case.account_id) or (
                not case.journal_id and case.account_id
            ):
                raise UserError(
                    _(
                        "Incorrect Accounting Settings.\n"
                        "Account and Journal should be set both or not set."
                    )
                )
