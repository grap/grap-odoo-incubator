# Copyright 2022 ACSONE SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class AccountMoveCreditNote(models.TransientModel):

    _name = "wizard.account_move_credit_notes.wallet"
    _description = "Credit Note By Wallet"

    account_wallet_type_id = fields.Many2one(
        comodel_name="account.wallet.type",
        string="Wallet type",
        required=True,
        ondelete="cascade",
    )

    amount = fields.Float(required=True)

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Customer", required=True, ondelete="cascade"
    )

    invoice_date = fields.Date(string="Invoice Date", default=fields.Date.today)

    def _prepare_move_values(self):
        line_values = self._prepare_move_line_values()
        values = {
            "partner_id": self.partner_id.id,
            "invoice_date": self.invoice_date,
            "move_type": "out_refund",
            "account_wallet_type_id": self.account_wallet_type_id.id,
            "invoice_line_ids": line_values,
        }
        return values

    def _prepare_move_line_values(self):
        credit_product = self.account_wallet_type_id.credit_note_product_id
        values = [
            (
                0,
                False,
                {
                    "product_id": credit_product.id,
                    "quantity": 1,
                    "price_unit": self.amount,
                    "name": credit_product.display_name,
                },
            )
        ]
        return values

    def apply(self):
        self.ensure_one()
        # Waiting for denis roussel response
        # https://github.com/OCA/wallet/pull/9#issuecomment-1206338548
        raise NotImplementedError()

    def __apply__(self):
        # the workaroung we designed is due to multiple factor
        # 1) account/account.move/_recompute_payment_terms_lines
        #       has not been designed to be extended
        # So we can't change the account easily
        # 2) the account on wallet is neither 'payable' nor 'receivable'
        # we can't rely on odoo when here is a change
        # so we found this solution in order to create a line on the right account
        old_account = self.partner_id.property_account_receivable_id
        try:
            self.partner_id.property_account_receivable_id = (
                self.account_wallet_type_id.account_id
            )

            values = self._prepare_move_values()
            move = self.env["account.move"].create(values)
            move.action_post()
        finally:
            self.partner_id.property_account_receivable_id = old_account

        return {
            "name": _("Credit Note"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": move.id,
        }
