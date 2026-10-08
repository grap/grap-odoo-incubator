# Copyright (C) 2023-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_id = fields.Many2one(default=lambda x: x._default_uom_id())

    uom_po_id = fields.Many2one(default=lambda x: x._default_uom_po_id())

    def _default_uom_id(self):
        """Overwrite the original function that returns 'Units'
        In our case, if there are many favorites, force user to decide.
        Otherwise, set the unique favorite unit of measure as the default one.
        (Except in install mode, to avoid errors and conflict with demo data)
        """
        result = self._get_default_uom_id()

        if self.env.context.get("install_mode"):
            return result

        if self.env.context.get("create_product_product"):
            # we are in the create section of the product.product model,
            # category has not been defined, and default value has been called
            # we avoid blocking and return result
            return result

        favorite_uoms = self.env["uom.uom"].search([("is_favorite", "=", True)])
        if len(favorite_uoms) == 1:
            return favorite_uoms[0].id

        return False

    def _default_uom_po_id(self):
        result = self._get_default_uom_po_id()

        if self.env.context.get("install_mode"):
            return result

        if self.env.context.get("create_product_product"):
            # we are in the create section of the product.product model,
            # category has not been defined, and default value has been called
            # we avoid blocking and return result
            return result

        favorite_uoms = self.env["uom.uom"].search([("is_favorite", "=", True)])
        if len(favorite_uoms) == 1:
            return favorite_uoms[0].id

        return False

    @api.constrains("uom_id")
    def _check_uom(self):
        # Disable check in test mode to avoid errors
        # if other modules create / update products with incorrect settings.
        if not tools.config["test_enable"] and self.filtered(
            lambda x: not x.uom_id.is_favorite
        ):
            raise ValidationError(_("You can not set this Unit of Measure."))
        return super()._check_uom()
