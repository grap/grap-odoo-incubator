# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Simple Pricelist module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields
from openerp.osv.orm import TransientModel
from openerp.addons import decimal_precision as dp


class productSimplePricelistItemUpdateWizard(TransientModel):
    _name = 'product.simple.pricelist.item.update.wizard'

    # Default Get Section
    def default_get(self, cr, uid, fields, context=None):
        pp_obj = self.pool['product.product']
        pplv_obj = self.pool['product.pricelist.version']
        res = super(productSimplePricelistItemUpdateWizard, self).default_get(
            cr, uid, fields, context=context)
        pp = pp_obj.browse(
            cr, uid, context['product_id'], context=context)
        pplv = pplv_obj.browse(
            cr, uid, context['pricelist_version_id'], context=context)

        res.update({
            'product_id': pp.id,
            'list_price': pp.list_price,
            'pricelist_id': pplv.pricelist_id.id,
            'pricelist_version_id': pplv.id,
        })
        return res

    # Column Section
    _columns = {
        'list_price': fields.float(
            'List Price', required=True, readonly=True,
            digits_compute=dp.get_precision('Product Price')),
        'pricelist_id': fields.many2one(
            'product.pricelist', 'Pricelist',
            required=True, readonly=True),
        'pricelist_version_id': fields.many2one(
            'product.pricelist.version', 'Pricelist Version',
            required=True, readonly=True),
        'product_id': fields.many2one(
            'product.product', 'Product', required=True, readonly=True),
        'specific_price': fields.float(
            'Price', required=True,
            digits_compute=dp.get_precision('Product Price')),
    }

    # Button Section
    def set_price(self, cr, uid, ids, context=None):
        pp_obj = self.pool['product.product']
        pplv_obj = self.pool['product.pricelist.version']
        ppli_obj = self.pool['product.pricelist.item']
        for pspiuw in self.browse(cr, uid, ids, context=context):
            pp = pp_obj.browse(cr, uid, pspiuw.product_id.id, context=context)
            pplv = pplv_obj.browse(
                cr, uid, pspiuw.pricelist_version_id.id, context=context)
            item_id = False
            for item in pplv.items_id:
                if item.product_id.id == pp.id:
                    item_id = item.id
            if item_id:
                if pspiuw.specific_price == 0:
                    # Unlink specific price
                    ppli_obj.unlink(cr, uid, [item_id], context=context)
                # Update specific price
                ppli_obj.write(cr, uid, [item_id], {
                    'price_surcharge': pspiuw.specific_price,
                    }, context=context)
            else:
                # Create new item
                ppli_obj.create(cr, uid, {
                    'name': pp.code,
                    'product_id': pspiuw.product_id.id,
                    'company_id': pplv.company_id.id,
                    'price_version_id': pplv.id,
                    'base': 1,
                    'price_discount': -1,
                    'price_surcharge': pspiuw.specific_price,
                }, context=context)

        return True
