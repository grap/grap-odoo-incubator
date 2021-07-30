# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from math import ceil

from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    package_qty = fields.Float(
        string="Package Quantity",
        default=0,
        help="The quantity of products in the supplier package."
        " You will always have to buy a multiple of this quantity.",
    )

    @api.multi
    def _get_quantity_according_package(self, product_qty, uom):
        self.ensure_one()
        # For the time being, Odoo is limited and doesn't
        # recover seller if the unit of the purchase order line is different
        # from the unit of the supplierinfo.
        # this function should be improved using uom arg,
        # when Odoo purchase module will be improved. (>12.0)
        if self.package_qty and product_qty % self.package_qty:
            return ceil(product_qty / self.package_qty) * self.package_qty
        else:
            return product_qty

    @api.onchange("package_qty")
    def onchange_package_qty(self):
        if self.package_qty:
            if self.package_qty > self.min_qty:
                self.min_qty = self.package_qty
            elif self.min_qty % self.package_qty:
                # check if min_qty is a multiple of package_qty
                self.min_qty = ceil(self.min_qty // self.package_qty) * self.package_qty

    @api.onchange("min_qty")
    def onchange_min_qty(self):
        if self.package_qty:
            if self.package_qty > self.min_qty:
                self.package_qty = self.min_qty
            elif self.min_qty % self.package_qty:
                # check if min_qty is a multiple of package_qty
                self.min_qty = ceil(self.min_qty / self.package_qty) * self.package_qty
