# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = "base.config.settings"

    multi_search_product_separator = fields.Char(
        string="Search Product Separator Character"
    )

    multi_search_product_separator_changed = fields.Boolean(
        compute="_compute_multi_search_product_separator_changed"
    )

    # Compute Section
    @api.multi
    @api.depends("multi_search_product_separator")
    def _compute_multi_search_product_separator_changed(self):
        current = self._get_multi_search_product_separator()
        for record in self:
            record.multi_search_product_separator_changed = bool(
                record.multi_search_product_separator != current
            )

    # Default Section
    @api.model
    def get_default_multi_search_product_separator(self, fields):
        return {
            "multi_search_product_separator": self._get_multi_search_product_separator()
        }

    # Setter Section
    @api.multi
    def set_multi_search_product_separator(self):
        self.ensure_one()
        config_obj = self.env["ir.config_parameter"]
        product_obj = self.env["product.product"]
        template_obj = self.env["product.template"]
        if self.multi_search_product_separator_changed:
            if self.multi_search_product_separator:
                config_obj.set_param(
                    "multi_search_product_separator",
                    self.multi_search_product_separator,
                )
                product_obj._multi_search_replace_all()
                template_obj._multi_search_replace_all()
            else:
                configs = config_obj.search(
                    [("key", "=", "multi_search_product_separator")]
                )
                configs.unlink()

    @api.model
    def _get_multi_search_product_separator(self):
        return self.env["ir.config_parameter"].get_param(
            "multi_search_product_separator", ""
        )
