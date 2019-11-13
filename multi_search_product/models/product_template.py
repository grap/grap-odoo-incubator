# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "multi.search.mixin"]

    _multi_search_separator_key_name = "multi_search.product_separator"

    # Overwrite Section
    @api.model
    def _multi_search_search_fields(self):
        return ["name", "default_code"]

    @api.model
    def _multi_search_write_fields(self):
        return ["name", "default_code"]
