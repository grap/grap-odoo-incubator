# Copyright (C) 2021-Today: Coop IT Easy (<http://coopiteasy.be>)
# @author: Rémy TAYMANS (<remy@coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    print_category_id = fields.Many2one(
        related="product_variant_id.print_category_id", readonly=False
    )

    to_print = fields.Boolean(related="product_variant_id.to_print", readonly=False)
