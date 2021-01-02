# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class SynchronizationMapping(models.Model):
    _name = "synchronization.mapping"
    _description = "Odoo Synchronization Mapping"

    model_id = fields.Many2one(
        comodel_name="ir.model", string="Model")

    internal_id = fields.Integer(string="Internal ID")

    external_id = fields.Integer(string="External ID")
