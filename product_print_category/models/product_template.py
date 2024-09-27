# Copyright (C) 2021-Today: Coop IT Easy (<http://coopiteasy.be>)
# @author: Rémy TAYMANS (<remy@coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "product.print.category.mixin"]

    # store this field (required for the related fields below)
    product_variant_id = fields.Many2one(store=True)

    print_category_id = fields.Many2one(
        related="product_variant_id.print_category_id", readonly=False
    )

    to_print = fields.Boolean(related="product_variant_id.to_print", readonly=False)

    @api.depends("product_variant_ids")
    def _compute_product_variant_id(self):
        # This is a very particular workaround for the following workflow:
        #
        # - Archive product.template.
        # - Duplicate product.template. <-- This method is called in this step.
        # - Unarchive duplicated product.template.
        #
        # If a product.template is archived, then its variants are also
        # archived. This means that accessing `product_variant_ids` outputs an
        # empty recordset, subsequently causing this compute function to wrongly
        # populate `product_variant_id` with null. By disabling `active_test`,
        # we prevent this problem.
        #
        # Upsteam bugfix in <https://github.com/odoo/odoo/pull/181811> targeted
        # at v15+.
        for p in self:
            # We do with_context() on each individual product instead of on
            # self, because doing it on self does not produce the desired result
            # in Odoo 12, somehow.
            p.product_variant_id = (
                p.with_context(active_test=False).product_variant_ids[:1].id
            )

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get("update_to_print_category", True):
            self._update_to_print_values(vals)
        return res
