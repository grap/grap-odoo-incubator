# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SynchronizationMapping(models.Model):
    _name = "synchronization.mapping"
    _description = "Odoo Synchronization Mapping"

    synchronization_data_id = fields.Many2one(
        comodel_name="synchronization.data",
        string="Synchronization Data",
        required=True,
        ondelete="cascade",
        readonly=True,
    )

    model_id = fields.Many2one(
        comodel_name="ir.model",
        related="synchronization_data_id.model_id",
        store=True,
        readonly=True,
    )

    internal_id = fields.Integer(string="Internal ID", readonly=True)

    external_id = fields.Integer(string="External ID", readonly=True)

    xml_id = fields.Char(string="XML ID", readonly=True)

    name = fields.Char(string="Name", readonly=True, compute="_compute_name")

    @api.depends("model_id.model", "internal_id")
    def _compute_name(self):
        for mapping in self:
            mapping.name = "{} - {}".format(
                mapping.synchronization_data_id.model_id.model, mapping.internal_id
            )
