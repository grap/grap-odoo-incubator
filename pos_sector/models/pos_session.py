# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Jean-Sébastien SUZANNE (js@hashbang.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.osv.expression import AND


class PosSession(models.Model):
    _inherit = "pos.session"

    def apply_sector_domain(self, domain):
        return AND(
            [
                domain,
                [
                    "|",
                    ("sector_id", "=", False),
                    ("sector_id", "in", self.config_id.sector_ids.ids),
                ],
            ]
        )

    def _loader_params_product_product(self):
        """Overload the loader to add in the domain the filter by sectors."""
        params = super()._loader_params_product_product()
        params["search_params"]["domain"] = self.apply_sector_domain(
            params["search_params"]["domain"]
        )
        return params

    def get_pos_ui_product_product_by_params(self, custom_search_params):
        if custom_search_params.get("domain"):
            custom_search_params["domain"] = self.apply_sector_domain(
                custom_search_params["domain"]
            )

        return super().get_pos_ui_product_product_by_params(custom_search_params)
