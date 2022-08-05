# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common
from odoo import tools
from odoo.modules.module import get_module_resource


def load_file(cr, module, *args):
    tools.convert_file(
        cr,
        "account_wallet",
        get_module_resource(module, *args),
        {},
        "init",
        False,
        "test",
    )


class WalletCommon(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(WalletCommon, cls).setUpClass()
        load_file(cls.cr, "account_wallet", "tests/data/", "account_wallet_data.xml")
        cls.AccountMove = cls.env["account.move"]
        cls.AccountWallet = cls.env["account.wallet"]
        cls.AccountPaymentRegister = cls.env["account.payment.register"]

        cls.wallet_account = cls.env.ref("account_wallet.wallet_account")
        cls.wallet_journal = cls.env.ref("account_wallet.wallet_journal")
        cls.wallet_type = cls.env.ref("account_wallet.wallet_type")
        cls.partner = cls.env.ref("base.res_partner_2")
        cls.sale_product = cls.env.ref("product.product_product_4d")

        cls.receivable_account = cls.env["account.account"].search(
            [("user_type_id.type", "=", "receivable")], limit=1
        )

        cls.wallet = cls.AccountWallet.create(
            {
                "wallet_type_id": cls.wallet_type.id,
            }
        )

    def _create_invoice_credit_wallet(self, credit_amount):
        """
        - Create an invoice to credit a wallet
        - post the invoice
        - check if the wallet is created (or associated)
        - return the invoice and the wallet
        """

        invoice = self.AccountMove.create(
            {
                "move_type": "out_invoice",
                "partner_id": self.env.ref("base.res_partner_2").id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "set 100 in my wallet",
                            "quantity": 1,
                            "price_unit": credit_amount,
                            "product_id": self.wallet_type.product_id.id,
                            "account_id": self.wallet_type.account_id.id,
                        },
                    )
                ],
            }
        )
        invoice.action_post()
        has_wallet = False
        for line in invoice.invoice_line_ids:
            if line.account_id.id == self.wallet_type.account_id.id:
                wallet = line.account_wallet_id
                self.assertTrue(wallet.wallet_type_id.id, self.wallet_type.id)
                has_wallet = True
        self.assertTrue(has_wallet)
        return invoice, wallet

    def _create_invoice_sale(self, move_type, amount):
        invoice = self.AccountMove.create(
            {
                "move_type": move_type,
                "partner_id": self.env.ref("base.res_partner_2").id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Invoice line",
                            "quantity": 1,
                            "price_unit": amount,
                            "product_id": self.sale_product.id,
                        },
                    )
                ],
            }
        )
        invoice.action_post()
        return invoice

    def _create_payment_move_wallet(self, debit_amount, wallet):
        """
        - create a payment move to debit a given wallet
        - post the payment move
        - check that the wallet has been correctly debited
        """
        old_wallet_balance = wallet.balance
        payment_move = self.AccountMove.create(
            {
                "journal_id": wallet.wallet_type_id.journal_id.id,
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": wallet.wallet_type_id.account_id.id,
                            "partner_id": wallet.partner_id.id,
                            "account_wallet_id": wallet.id,
                            "name": "payment with my wallet",
                            "debit": debit_amount,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "account_id": self.receivable_account.id,
                            "name": "payment with my wallet",
                            "credit": debit_amount,
                        },
                    ),
                ],
            }
        )
        self.assertEqual(wallet.balance, old_wallet_balance)
        payment_move.action_post()
        self.assertEqual(wallet.balance, old_wallet_balance - debit_amount)
        return payment_move

    def _create_payment_move_wallet_via_wizard(self, invoice, debit_amount, wallet):
        """
        - Use the 'account.payment.register' wizard to pay an invoice
          with a 'wallet' journal
        - check that the wallet has been correctly debited
        """
        payment_wizard = self.AccountPaymentRegister.with_context(
            active_model="account.move",
            active_ids=invoice.ids,
        ).create(
            {
                "journal_id": wallet.wallet_type_id.journal_id.id,
                "account_wallet_id": wallet.id,
                "amount": debit_amount,
            }
        )
        payment_wizard.action_create_payments()
