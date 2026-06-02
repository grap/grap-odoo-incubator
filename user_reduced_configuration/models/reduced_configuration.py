# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import _, api, fields, models


class ResReducedConfigSettings(models.Model):
    _name = "reduced.configuration"
    _description = "Reduced Configurations"

    name = fields.Char(compute="_compute_name", store=True)

    field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        domain=lambda x: x._domain_field_id(),
    )

    field_qty = fields.Integer(store=True, compute="_compute_field_qty")

    group_id = fields.Many2one(required=True, comodel_name="res.groups")

    @api.depends("group_id")
    def _compute_name(self):
        for configuration in self:
            configuration.name = _(
                "Configuration for %(group_name)s",
                group_name=configuration.group_id
                and configuration.group_id.name
                or "/",
            )

    @api.depends("field_ids")
    def _compute_field_qty(self):
        for configuration in self:
            configuration.field_qty = len(configuration.field_ids)

    def _domain_field_id(self):
        return [
            (
                "name",
                "not in",
                [
                    "id",
                    "__last_update",
                    "display_name",
                    "create_uid",
                    "create_date",
                    "write_uid",
                    "write_date",
                ],
            ),
            ("name", "not ilike", "module_"),
            ("model", "=", "res.config.settings"),
        ]
