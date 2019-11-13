# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class BaseConfigSettings(models.TransientModel):
    _inherit = "base.config.settings"

    multi_search_partner_separator = fields.Char(string="Partner Separator")

    multi_search_partner_separator_changed = fields.Boolean(
        compute="_compute_multi_search_partner_separator_changed"
    )

    # Compute Section
    @api.multi
    @api.depends("multi_search_partner_separator")
    def _compute_multi_search_partner_separator_changed(self):
        current = self._get_multi_search_partner_separator()
        for record in self:
            record.multi_search_partner_separator_changed = bool(
                record.multi_search_partner_separator != current
            )

    # Default Section
    @api.model
    def get_default_multi_search_partner_separator(self, fields):
        return {
            "multi_search_partner_separator": self._get_multi_search_partner_separator()
        }

    # Setter Section
    @api.multi
    def set_multi_search_partner_separator(self):
        self.ensure_one()
        config_obj = self.env["ir.config_parameter"]
        partner_obj = self.env["res.partner"]
        if self.multi_search_partner_separator_changed:
            if self.multi_search_partner_separator:
                config_obj.set_param(
                    "multi_search_partner_separator",
                    self.multi_search_partner_separator,
                )
                partner_obj._multi_search_replace_all()
            else:
                configs = config_obj.search(
                    [("key", "=", "multi_search_partner_separator")]
                )
                configs.unlink()

    @api.model
    def _get_multi_search_partner_separator(self):
        return self.env["ir.config_parameter"].get_param(
            "multi_search_partner_separator", ""
        )
