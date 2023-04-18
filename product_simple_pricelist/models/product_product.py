# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = "product.product"

    specific_pricelist_item_id = fields.Many2one(
        comodel_name="product.pricelist.item",
        compute="_compute_pricelist_price",
    )

    pricelist_price = fields.Float(
        string="Pricelist Price",
        compute="_compute_pricelist_price",
        digits=dp.get_precision("Pricelist Price"),
        inverse="_inverse_pricelist_price",
    )

    pricelist_price_difference_rate = fields.Float(
        string="Difference (%)",
        compute="_compute_pricelist_price",
        digits=dp.get_precision("Discount"),
    )

    variant_item_ids = fields.One2many(
        string="Variant Pricelist Items",
        comodel_name="product.pricelist.item",
        inverse_name="product_id",
        copy=True,
    )

    def _get_pricelist_item_by_pricelist(self, pricelist):
        self.ensure_one()
        items = pricelist.item_ids.filtered(
            lambda x: x.applied_on == "0_product_variant"
            and x.product_id.id == self.id
            and x.compute_price == "fixed"
        )
        return items and items[0] or False

    def _compute_pricelist_price(self):
        pricelist_id = self._context.get("pricelist_id", False)
        if not pricelist_id:
            return
        pricelist = self.env["product.pricelist"].browse(pricelist_id)
        for product in self:
            item = product._get_pricelist_item_by_pricelist(pricelist)
            product.specific_pricelist_item_id = item
            if item:
                product.pricelist_price = item.fixed_price
            else:
                product.pricelist_price = pricelist._compute_price_rule(
                    [(product, 1.0, False)]
                )[product.id][0]

            product.pricelist_price_difference_rate = (
                product.lst_price
                and ((product.pricelist_price - product.lst_price) / product.lst_price)
                * 100
                or 0.0
            )

    def _inverse_pricelist_price(self):
        ProductPricelistItem = self.env["product.pricelist.item"]
        pricelist_id = self._context.get("pricelist_id", False)
        if not pricelist_id:
            raise UserError(
                _("Unabled to set Pricelist Price if pricelist is not defined")
            )
        pricelist = self.env["product.pricelist"].browse(pricelist_id)

        for product in self:
            item = product._get_pricelist_item_by_pricelist(pricelist)
            if item:
                # Update price if item exist
                item.fixed_price = product.pricelist_price
            else:
                # Create a new item
                ProductPricelistItem.create(
                    {
                        "pricelist_id": pricelist.id,
                        "applied_on": "0_product_variant",
                        "product_id": product.id,
                        "compute_price": "fixed",
                        "fixed_price": product.pricelist_price,
                    }
                )

    def delete_pricelist_price(self):
        pricelist_id = self._context.get("pricelist_id", False)
        if not pricelist_id:
            raise UserError(
                _("Unabled to set Pricelist Price if pricelist is not defined")
            )
        pricelist = self.env["product.pricelist"].browse(pricelist_id)
        for product in self:
            item = product._get_pricelist_item_by_pricelist(pricelist)
            if item:
                item.unlink()
