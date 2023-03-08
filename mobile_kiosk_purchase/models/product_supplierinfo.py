# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from math import ceil

from odoo import api, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.multi
    def _get_quantity_according_multiplier(self, product_qty, uom):
        self.ensure_one()
        # For the time being, Odoo is limited and doesn't
        # recover seller if the unit of the purchase order line is different
        # from the unit of the supplierinfo.
        # this function should be improved using uom arg,
        # when Odoo purchase module will be improved. (>12.0)
        if self.multiplier_qty and product_qty % self.multiplier_qty:
            return ceil(product_qty / self.multiplier_qty) * self.multiplier_qty
        else:
            return product_qty
