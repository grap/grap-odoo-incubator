# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    racking_ids = fields.Many2many(
        string="Racking",
        comodel_name="stock.racking",
        compute=lambda x: x._compute_template_field_from_variant_field("racking_ids"),
        inverse=lambda x: x._set_product_variant_field("racking_ids"),
        readonly=False,
        domain=[("type", "=", "normal")],
    )

    def _get_related_fields_variant_template(self):
        res = super()._get_related_fields_variant_template()
        res.append("racking_ids")
        return res
