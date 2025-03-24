# Copyright (C) 2023-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductUom(models.Model):
    _inherit = "uom.uom"

    is_favorite = fields.Boolean(
        string="Favorite",
        company_dependent=True,
        help="If this field is unchecked, the uom will"
        " be hidden when searching uom in a drop-down list"
        " like in the product form view.",
    )

    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        args = list(args or [])
        if self.env.context.get("display_only_favorite", False):
            args += [("is_favorite", "=", True)]
        return super()._name_search(
            name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid
        )
