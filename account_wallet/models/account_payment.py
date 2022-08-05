# Copyright 2021 ACSONE SA/NV (https://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountPayment(models.Model):

    _inherit = "account.payment"

    account_wallet_id = fields.Many2one(
        comodel_name="account.wallet",
    )

    def _get_liquidity_move_line_vals(self, amount):
        res = super()._get_liquidity_move_line_vals(amount)
        if self.account_wallet_id:
            res.update({"account_wallet_id": self.account_wallet_id.id})
        return res
