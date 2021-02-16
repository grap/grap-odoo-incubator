# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    editable_by_product = fields.Boolean(
        string="Editable By Product",
        oldname="is_simple",
        help="Check this box if you want to edit this" " pricelist by product",
    )

    # View Section
    @api.multi
    def button_edit_pricelist_by_product(self):
        self.ensure_one()
        action = self.env.ref(
            "product_simple_pricelist.action_edit_pricelist_by_product"
        )
        result = action.read()[0]
        context = safe_eval(result.get("context", "{}"))
        context.update({"pricelist_id": self.id})
        result.update(
            {
                "name": _("Edit Pricelist '%s' By Product") % (self.name),
                "context": str(context),
            }
        )

        return result
