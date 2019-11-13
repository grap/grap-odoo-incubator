# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "multi.search.mixin"]

    # Overwrite Section
    @api.model
    def _multi_search_search_fields(self):
        return ["name", "default_code"]

    @api.model
    def _multi_search_write_fields(self):
        return ["name", "default_code"]

    @api.model
    def _multi_search_separator(self):
        setting_obj = self.env["base.config.settings"]
        return setting_obj._get_multi_search_product_separator()

    @api.multi
    def write(self, vals):
        """Overload in this part, because write function is not called
        in mixin model. TODO: Check if this weird behavior still occures
        in more recent Odoo versions.
        """
        if self._multi_search_separator():
            vals = self._multi_search_replace_dict(vals, True)
        return super(ProductTemplate, self).write(vals)
