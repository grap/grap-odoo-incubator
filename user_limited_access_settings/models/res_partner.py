# Copyright 2024 Sylvain LE GAL - GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    signup_expiration = fields.Datetime(
        groups="base.group_erp_manager,"
        "user_limited_access_settings.group_limited_settings"
    )

    signup_token = fields.Char(
        groups="base.group_erp_manager,"
        "user_limited_access_settings.group_limited_settings"
    )

    signup_type = fields.Char(
        groups="base.group_erp_manager,"
        "user_limited_access_settings.group_limited_settings"
    )
