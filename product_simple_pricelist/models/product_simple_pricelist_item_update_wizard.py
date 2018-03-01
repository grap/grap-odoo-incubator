# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.addons import decimal_precision as dp


class productSimplePricelistItemUpdateWizard(models.TransientModel):
    _name = 'product.simple.pricelist.item.update.wizard'

    # Column Section
    pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist',
        required=True, readonly=True)

    pricelist_version_id = fields.Many2one(
        comodel_name='product.pricelist.version')

    product_id = fields.Many2one(
        'product.product', 'Product', required=True, readonly=True)

    list_price = fields.Float(
        string='List Price', required=True, readonly=True,
        digits_compute=dp.get_precision('Product Price'))

    specific_price = fields.Float(
        'Price', required=True,
        digits_compute=dp.get_precision('Product Price'))

    # Default Get Section
    @api.model
    def default_get(self, fields):
        product_obj = self.env['product.product']
        version_obj = self.env['product.pricelist.version']
        res = super(productSimplePricelistItemUpdateWizard, self).default_get(
            fields)
        context = self.env.context
        product = product_obj.browse(context.get('product_id', False))
        version = version_obj.browse(
            context.get('pricelist_version_id', False))
        res.update({
            'product_id': product.id,
            'list_price': product.list_price,
            'pricelist_id': version.pricelist_id.id,
            'pricelist_version_id': version.id,
        })
        return res

    # Button Section
    @api.multi
    def set_price(self):
        self.ensure_one()
        item_obj = self.env['product.pricelist.item']

        # Search Existing pricelist item
        found_item = False
        for item in self.pricelist_version_id.items_id:
            if item.product_id.id == self.product_id.id:
                found_item = item

        if found_item:
            if self.specific_price == 0:
                # Unlink specific price
                found_item.unlink()
            else:
                # Update specific price
                found_item.price_surcharge = self.specific_price
        else:
            # Create new item
            item_obj.create(self._prepare_pricelist_item())

        return True

    # Custom Section
    @api.multi
    def _prepare_pricelist_item(self):
        self.ensure_one()
        return {
            'name': self.product_id.code,
            'product_id': self.product_id.id,
            'company_id': self.pricelist_version_id.company_id.id,
            'price_version_id': self.pricelist_version_id.id,
            'base': 1,
            'price_discount': -1,
            'price_surcharge': self.specific_price,
        }
