# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_package_id = fields.Many2one(
        comodel_name="uom.uom", string="Package Unit of Measure"
    )

    uom_package_qty = fields.Float(
        string="Package Quantity",
        default=0,
    )

    @api.model
    def _round_package_quantity(self, qty, uom_package_qty, uom_package_id, uom_id):
        new_qty = qty
        warning = False

        # Check if quantity is a multiple of package_qty
        if uom_package_qty and (qty % uom_package_qty) != 0:
            new_qty = ((qty // uom_package_qty) + 1) * uom_package_qty
            warning = {
                "title": _("Warning!"),
                "message": _(
                    "The quantity has been rounded to : %s X %s,"
                    " due to package condition."
                )
                % (new_qty, uom_package_id and uom_package_id.name or uom_id.name),
            }
        return {
            "qty": new_qty,
            "warning": warning,
        }

    @api.model
    def _counvert_package_qty(self, qty, uom_package_id, uom_id):
        # Convert to the target UoM if required
        if uom_package_id and uom_package_id != uom_id:
            return uom_package_id._compute_quantity(
                qty, uom_id, rounding_method="HALF-UP"
            )
        return qty
