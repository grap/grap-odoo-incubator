# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

_SUFFIX_LENGTH = 6


class ProductProduct(models.Model):
    _inherit = "product.product"

    default_code = fields.Char(readonly=True)

    # Overload Section
    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._set_default_code()
        return res

    # Custom Section
    @api.multi
    def _set_default_code(self):
        IrSequence = self.env["ir.sequence"]
        for product in self:
            product.default_code = IrSequence.next_by_code(
                "product_product.default_code"
            )
