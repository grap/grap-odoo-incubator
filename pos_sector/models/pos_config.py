# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    sector_ids = fields.Many2many(string="Sectors", comodel_name="pos.sector")

    def get_limited_products_loading(self, fields):
        return super(
            PosConfig, self.with_context(limit_to_pos_sector_ids=self.sector_ids.ids)
        ).get_limited_products_loading(fields)
