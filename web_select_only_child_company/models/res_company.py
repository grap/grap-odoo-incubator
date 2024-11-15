# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    all_child_ids = fields.One2many(
        comodel_name="res.company", compute="_compute_all_child_ids", recursive=True
    )

    @api.depends("child_ids.all_child_ids")
    def _compute_all_child_ids(self):
        for company in self:
            company.all_child_ids = company.mapped("child_ids") | company.mapped(
                "child_ids.all_child_ids"
            )
