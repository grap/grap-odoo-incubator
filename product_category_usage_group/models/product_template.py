# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import Warning as UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Overload Section
    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        res._check_usage_product_category(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        self._check_usage_product_category(vals)
        return res

    # Custom Section
    @api.multi
    def _check_usage_product_category(self, vals):
        ProductCategory = self.env["product.category"]
        if vals.get("categ_id", False):
            category = ProductCategory.browse(vals["categ_id"])
            group = category.usage_group_id
            if group and group.id not in self.env.user.groups_id.ids:
                raise UserError(
                    _(
                        "You can not use the product category '%s' because"
                        " you're not member of the group '%s'."
                    )
                    % (category.name, group.name)
                )
