# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    wallet_balance = fields.Monetary(
        compute="_compute_wallet_balance",
    )

    wallet_ids = fields.One2many(
        comodel_name="account.wallet",
        inverse_name="partner_id",
    )

    @api.depends("wallet_ids.balance")
    def _compute_wallet_balance(self):
        for partner in self:
            partner.wallet_balance = sum(partner.wallet_ids.mapped("balance"))
