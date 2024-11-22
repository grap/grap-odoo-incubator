# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ModelCreateRecursiveMixin(models.Model):
    _name = "model.create.recursive.mixin"
    _description = "model.create.recursive.mixin"
    _inherit = ["create.recursive.mixin"]
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"

    name = fields.Char()

    parent_id = fields.Many2one(comodel_name="model.create.recursive.mixin")

    parent_path = fields.Char(index=True, unaccent=False)

    complete_name = fields.Char(
        compute="_compute_complete_name", recursive=True, store=True
    )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = (
                    f"{category.parent_id.complete_name} / {category.name}"
                )
            else:
                category.complete_name = category.name

    # @api.model
    # def name_create(self, name):
    #     return self._name_create(name)
