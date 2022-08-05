# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    is_enabled_wallet = fields.Boolean(
        string="Has Payment Wallet Method", compute="_compute_is_enabled_wallet"
    )

    def _compute_is_enabled_wallet(self):
        for config in self:
            config.is_enabled_wallet = config.journal_ids.filtered(
                lambda x: x.is_wallet
            )
