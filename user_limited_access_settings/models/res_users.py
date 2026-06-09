# Copyright 2024 Sylvain LE GAL - GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    role_line_ids = fields.One2many(
        groups="base.group_erp_manager,user_limited_access_settings.group_limited_settings",
    )

    role_ids = fields.One2many(
        groups="base.group_erp_manager,user_limited_access_settings.group_limited_settings",
    )

    @api.constrains("groups_id")
    def _check_escalation(self):
        # ignore constrains for sudo() call
        if self.env.is_admin():
            return
        missing_groups = self.env["res.groups"]
        allowed_groups = (
            self.env.user.groups_id
            | self.env.ref("base.group_user")
            | self.env.ref("base.group_portal")
            | self.env.ref("base.group_public")
        )
        for group in self.groups_id:
            if group not in allowed_groups:
                missing_groups |= group

        if missing_groups:
            raise ValidationError(
                _(
                    "The user '%(username)s' lack some rights to"
                    " do this action. \n"
                    "Here are the groups needed :\n- %(group_names)s",
                    username=str(self.env.user.name),
                    group_names="\n- ".join([x.display_name for x in missing_groups]),
                )
            )
