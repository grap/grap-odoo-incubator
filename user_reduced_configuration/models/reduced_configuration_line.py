# # Part of Odoo. See LICENSE file for full copyright and licensing details.


# from odoo import fields, models


# class ResReducedConfigSettingsLine(models.Model):
#     _name = "reduced.configuration.line"
#     _description = "Reduced Configuration Lines"

#     field_id = fields.Many2one(
#         required=True,
#         comodel_name="ir.model.fields",
#         domain=lambda x: x._domain_field_id(),
#         ondelete="cascade",
#     )

#     field_ttype = fields.Selection(related="field_id.ttype")

#     field_modules = fields.Char(related="field_id.modules")

#     field_help = fields.Text(related="field_id.help")

#     group_id = fields.Many2one(required=True, comodel_name="res.groups")

#     def _domain_field_id(self):
#         return [
#             (
#                 "name",
#                 "not in",
#                 [
#                     "id",
#                     "__last_update",
#                     "display_name",
#                     "create_uid",
#                     "create_date",
#                     "write_uid",
#                     "write_date",
#                 ],
#             ),
#             ("name", "not ilike", "module_"),
#             ("model", "=", "res.config.settings"),
#         ]
