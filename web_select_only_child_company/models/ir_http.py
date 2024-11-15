# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        result = super().session_info()
        if self.env.user.has_group("base.group_user"):
            for company in self.env.user.company_ids:
                result["user_companies"]["allowed_companies"][company.id][
                    "all_child_ids"
                ] = company.all_child_ids.ids
        return result
