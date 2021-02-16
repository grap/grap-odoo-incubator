# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PosSector(models.Model):
    _name = "pos.sector"
    _description = "Point of Sale Sectors"

    # Columns section
    name = fields.Char(required=True)

    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda s: s._default_company_id(),
    )

    # Default section
    def _default_company_id(self):
        return self.env.user.company_id.id
