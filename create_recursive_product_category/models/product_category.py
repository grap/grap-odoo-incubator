# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductCategory(models.Model):
    _name = "product.category"
    _inherit = ["product.category", "create.recursive.mixin"]

    @api.model
    def name_create(self, name):
        return self._name_create(name)
