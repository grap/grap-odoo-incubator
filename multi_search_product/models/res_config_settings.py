# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    multi_search_product_separator = fields.Char(
        string="Search Product Separator Character",
        config_parameter="multi_search.product_separator"
    )

    multi_search_product_separator_changed = fields.Boolean(
        compute="_compute_multi_search_product_separator_changed"
    )

    # Compute Section
    @api.multi
    @api.depends('multi_search_product_separator')
    def _compute_multi_search_product_separator_changed(self):
        current = self.env['ir.config_parameter'].get_param(
            'multi_search.product_separator')
        for record in self:
            record.multi_search_product_separator_changed = bool(
                record.multi_search_product_separator != current)

    @api.multi
    def set_values(self):
        ProductProduct = self.env["product.product"]
        ProductTemplate = self.env["product.template"]
        replace_all = any(
            self.mapped('multi_search_product_separator_changed'))
        res = super().set_values()
        if replace_all:
            ProductProduct._multi_search_replace_all()
            ProductTemplate._multi_search_replace_all()
        return res
