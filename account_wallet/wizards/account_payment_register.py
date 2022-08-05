# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):

    _inherit = "account.payment.register"

    account_wallet_id = fields.Many2one(
        comodel_name="account.wallet",
        string="Wallet",
        ondelete="cascade",
    )

    def _create_payment_vals_from_wizard(self):
        res = super()._create_payment_vals_from_wizard()
        res["account_wallet_id"] = self.account_wallet_id.id
        return res
