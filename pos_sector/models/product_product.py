# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.osv.expression import AND


class ProductProduct(models.Model):
    _inherit = "product.product"

    def search_read(self, domain, *args, **kwargs):
        sector_ids = self.env.context.get("limit_to_pos_sector_ids", [])
        if sector_ids:
            domain = AND([domain, [("sector_id", "in", sector_ids + [False])]])

        return super().search_read(domain, *args, **kwargs)
