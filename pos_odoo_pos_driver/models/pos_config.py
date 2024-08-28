# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    # Columns section
    use_odoo_pos_driver = fields.Boolean()
