# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "multi.search.mixin"]

    _multi_search_separator_key_name = "multi_search.partner_separator"

    # Overwrite Section
    @api.model
    def _multi_search_search_fields(self):
        return ["name", "display_name", "email"]

    @api.model
    def _multi_search_write_fields(self):
        return ["name", "email"]
