# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    is_wallet = fields.Boolean(
        string="Is Wallet",
        compute="_compute_is_wallet",
    )

    account_wallet_type_ids = fields.One2many(
        comodel_name="account.wallet.type",
        inverse_name="journal_id",
        readonly=True,
    )

    @api.depends("account_wallet_type_ids.journal_id")
    def _compute_is_wallet(self):
        for journal in self:
            journal.is_wallet = len(journal.account_wallet_type_ids)
