# Copyright (C) 2023-Today: GRAP (<http://www.grap.coop/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_id = fields.Many2one(default=lambda x: x._get_default_uom_id())

    def _get_default_uom_id(self):
        """Overwrite the original function that returns 'Units'
        In our case, if there are many favorites, force user to decide.
        Otherwise, set the unique favorite unit of measure as the default one.
        """
        favorite_uoms = self.env["uom.uom"].search([("is_favorite", "=", True)])
        if len(favorite_uoms) == 1:
            return favorite_uoms[0].id
        return False

    @api.constrains("uom_id")
    def _check_uom(self):
        if self.filtered(lambda x: not x.uom_id.is_favorite):
            raise ValidationError(_("You can not set this Unit of Measure."))
        return super()._check_uom()
