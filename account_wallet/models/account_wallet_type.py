# © 2015  Laetitia Gangloff, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountWalletType(models.Model):
    _name = "account.wallet.type"
    _description = "Wallet Type"
    _check_company_auto = True

    name = fields.Char(translate=True, required=True)
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Wallet Sequence",
        copy=False,
        check_company=True,
        help="This field contains the information related to the numbering "
        "of the wallet of this type.",
        required=True,
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        ondelete="restrict",
        index=True,
        required=True,
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        ondelete="restrict",
        help="Journal use to empty the wallet",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        ondelete="restrict",
        help="Product use to fill the wallet",
        required=True,
        domain="[('type', '=', 'service')]",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.user.company_id,
        required=True,
    )

    automatic_nominative_creation = fields.Boolean(
        help="Check this box if you want to automaticaly create nominative wallets"
        " (related to a partner) when selling products related to a wallet type."
    )

    only_nominative = fields.Boolean(
        help="Check this box if you want to ensure all the wallets have"
        " a partner defined. Note that enable this feature will prevent to use"
        " wallet for 'Gifts' (Customer pay a wallet to make a gift to another customer)"
    )

    credit_note_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Credit Note Product",
        help="This product will be used in the 'Credit Note with Wallet' Wizard",
        domain="[('type', '=', 'service')]",
    )

    _sql_constraints = [
        (
            "product_wallet_type_uniq",
            "unique(product_id, company_id)",
            "A wallet type with the product already exists",
        ),
        (
            "account_wallet_uniq",
            "unique(account_id)",
            "A wallet type with this account already exists",
        ),
    ]

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id and not self.account_id:
            self.account_id = self.product_id._get_product_accounts()["income"]

    @api.onchange("only_nominative")
    def onchange_only_nominative(self):
        if self.only_nominative:
            self.automatic_nominative_creation = True

    @api.constrains("only_nominative", "automatic_nominative_creation")
    def _check_only_nominative_automatic_nominative_creation(self):
        types = self.filtered(
            lambda x: x.only_nominative and not x.automatic_nominative_creation
        )
        if types:
            raise ValidationError(
                _(
                    "You have to check 'Automatic Nominative Creation'"
                    "if 'Only Nominative' is checked."
                )
            )
