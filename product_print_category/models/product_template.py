# Copyright (C) 2021-Today: Coop IT Easy (<http://coopiteasy.be>)
# @author: Rémy TAYMANS (<remy@coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "product.print.category.mixin"]

    print_category_id = fields.Many2one(
        related="product_variant_id.print_category_id", readonly=False
    )

    to_print = fields.Boolean(related="product_variant_id.to_print", readonly=False)

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if not self.env.context.get("do_not_update_to_print_category", False):
            self._update_to_print_values(vals)
        return res
