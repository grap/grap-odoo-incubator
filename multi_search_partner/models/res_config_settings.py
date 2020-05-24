# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    multi_search_partner_separator = fields.Char(
        string="Search Partner Separator Character",
        config_parameter="multi_search.partner_separator"
    )

    multi_search_partner_separator_changed = fields.Boolean(
        compute="_compute_multi_search_partner_separator_changed"
    )

    # Compute Section
    @api.multi
    @api.depends("multi_search_partner_separator")
    def _compute_multi_search_partner_separator_changed(self):
        current = self.env['ir.config_parameter'].sudo().get_param(
            'multi_search.partner_separator')
        for record in self:
            record.multi_search_partner_separator_changed = bool(
                record.multi_search_partner_separator != current)

    @api.multi
    def set_values(self):
        ResPartner = self.env["res.partner"]
        replace_all = any(
            self.mapped('multi_search_partner_separator_changed'))
        res = super().set_values()
        if replace_all:
            ResPartner._multi_search_replace_all()
        return res
