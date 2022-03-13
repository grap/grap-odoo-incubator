# Copyright (C) 2021-Today: Coop IT Easy (<http://coopiteasy.be>)
# @author: Rémy TAYMANS (<remy@coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    print_category_id = fields.Many2one(
        related="product_variant_id.print_category_id", readonly=False
    )

    to_print = fields.Boolean(related="product_variant_id.to_print", readonly=False)

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get("do_not_update_to_print_category", False):
            return res
        template_ids = []
        # Set 'To print' if we change one field choosen in print_category
        for template in self.filtered(lambda x: x.print_category_id):
            triggering_fields = template.print_category_id.field_ids.mapped("name") + [
                "print_category_id"
            ]
            if len(list(set(vals.keys()) & set(triggering_fields))):
                template_ids.append(template.id)
        templates = self.browse(template_ids)
        super(ProductTemplate, templates).write({"to_print": True})
        return res
