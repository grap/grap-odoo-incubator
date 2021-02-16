# Copyright (C) 2020-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    # Fields Section
    type = fields.Selection(
        selection=[("normal", "Normal"), ("view", "View")],
        default="normal",
        string="Type",
        required=True,
    )
