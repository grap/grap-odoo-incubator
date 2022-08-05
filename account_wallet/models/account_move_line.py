# © 2015  Laetitia Gangloff, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    account_wallet_id = fields.Many2one(
        comodel_name="account.wallet",
        string="Wallet",
        ondelete="restrict",
        index=True,
    )

    def _get_computed_account(self):
        if self.account_wallet_id:
            return self.account_wallet_id.wallet_type_id.account_id
        return super()._get_computed_account()

    @api.onchange("account_wallet_id")
    def _onchange_account_wallet_id(self):
        for line in self.filtered("account_wallet_id"):
            line.account_id = line._get_computed_account()
            partner = line.account_wallet_id.partner_id
            if partner:
                line.partner_id = partner

    def create_or_set_wallet(self):
        AccountWallet = self.env["account.wallet"]
        AccountWalletType = self.env["account.wallet.type"]

        # check if account/partner is linked to a wallet and assign it
        # if it the case
        for move_line in self.filtered(lambda x: x.partner_id):
            wallet_domain = [
                ("wallet_type_id.account_id", "=", move_line.account_id.id),
                ("partner_id", "=", move_line.partner_id.id),
            ]
            wallet = AccountWallet.search(wallet_domain)
            if wallet:
                move_line.write({"account_wallet_id": wallet.id})

        # Create new wallet, if the account match with the account if a wallet_type
        for move_line in self.filtered(lambda x: not x.account_wallet_id):
            wallet_type = AccountWalletType.search(
                [("account_id", "=", move_line.account_id.id)]
            )
            if not wallet_type:
                continue
            move_line.account_wallet_id = AccountWallet.create(
                move_line._prepare_account_wallet_values(wallet_type)
            )

    def _prepare_account_wallet_values(self, wallet_type):
        self.ensure_one()
        vals = {
            "wallet_type_id": wallet_type.id,
        }
        if wallet_type.automatic_nominative_creation:
            vals.update(
                {
                    "partner_id": self.partner_id.id,
                }
            )
        return vals

    @api.constrains("account_wallet_id", "account_id")
    def _check_wallet_account(self):
        """Account must correspond to wallet account"""
        incorrect_lines = self.filtered(
            lambda x: x.account_wallet_id
            and x.account_wallet_id.wallet_type_id.account_id != x.account_id
        )
        if incorrect_lines:
            msg = []
            for line in incorrect_lines:
                msg.append(
                    _(
                        "The move line account %s doesn't correspond to the wallet account %s"
                    )
                    % (
                        line.account_id.display_name,
                        line.account_wallet_id.wallet_type_id.account_id.display_name,
                    )
                )
            raise ValidationError("\n".join(msg))
