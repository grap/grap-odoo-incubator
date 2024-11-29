# Copyright 2024 Sylvain LE GAL - GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.constrains("groups_id")
    def _check_escalation(self):
        if self.env.user._is_admin():
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
                        "You can set the group '%(group_names)s'"
                        " to users, because you are not member of those groups.",
                        group_names=" , ".join(
                            [x.display_name for x in missing_groups]
                        ),
                    )
                )

    # def write(self, vals):
    #     print("write", self.ids, vals)
    #     if not self.env.user.has_privilege_escalation:
    #         group_ids = []
    #         for k, v in vals.items():
    #             if k.startswith("in_group_") and v:
    #                 group_ids.append(int(k.split("in_group_")[1]))
    #         print("group_ids", group_ids)
    #         for group_id in group_ids:
    #             if group_id not in self.env.user.groups_id.ids:
    #                 group = self.env["res.groups"].browse(group_id)
    #                 raise ValidationError(
    #                     _(
    #                         "You can set the group '%(group_name)s'"
    #                         " to users, because you are not member of this group.",
    #                         group_name=group.display_name,
    #                     )
    #                 )

    #     # Peut être utiliser une contrainte ?

    #     return super().write(vals)
