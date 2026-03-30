# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    reduced_configuration_line_ids = fields.One2many(
        comodel_name="reduced.configuration.line", inverse_name="group_id"
    )
