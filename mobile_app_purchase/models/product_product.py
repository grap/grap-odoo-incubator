# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class ProductProduct(Model):
    _inherit = 'product.product'

    _SCAN_TO_PURCHASE_MANDATORY_FIELDS = ['id', 'name', 'ean13']

    def _scan_to_purchase_product_fields(self, cr, uid, context=None):
        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid, context=context).company_id
        return [x.name for x in company.scan_purchase_product_fields_ids]

    def _scan_to_purchase_supplierinfo_fields(self, cr, uid, context=None):
        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid, context=context).company_id
        return [x.name for x in company.scan_purchase_supplierinfo_fields_ids]

    def scan_to_purchase_load_product(self, cr, uid, context=None):
        def _get_field_name(pool, cr, uid, field, model=False):
            translation_obj = self.pool['ir.translation']
            # Determine model name
            if not model:
                if field in pool.pool['product.product']._columns:
                    model = 'product.product'
                else:
                    model = 'product.template'
            # Get translation if defined
            translation_ids = translation_obj.search(cr, uid, [
                ('lang', '=', context['lang']),
                ('type', '=', 'field'),
                ('name', '=', '%s,%s' % (model, field))],
                context=context)
            if translation_ids:
                return translation_obj.browse(
                    cr, uid, translation_ids[0], context=context).value
            else:
                return pool.pool[model]._columns[field].string

        product_fields = self._scan_to_purchase_product_fields(
            cr, uid, context=context)
        supplierinfo_fields = self._scan_to_purchase_supplierinfo_fields(
            cr, uid, context=context)

        res = {}
        product_ids = self.search(
            cr, uid, [('ean13', '!=', False)], context=context)
        products = self.browse(cr, uid, product_ids, context=context)
        for product in products:
            res[product.ean13] = {}
            # Add product fields
            for field in self._SCAN_TO_PURCHASE_MANDATORY_FIELDS:
                res[product.ean13][field] = getattr(product, field)

            for field in product_fields:
                if field[-3:] == '_id':
                    res[product.ean13][field] = {
                        'id': getattr(product, field).id,
                        'value': getattr(product, field).name,
                        'field_name': _get_field_name(self, cr, uid, field),
                    }
                else:
                    res[product.ean13][field] = {
                        'value': getattr(product, field),
                        'field_name': _get_field_name(self, cr, uid, field),
                    }

            # Add supplierinfo fields
            res[product.ean13]['seller_ids'] = {}
            if supplierinfo_fields:
                for supplierinfo in product.product_tmpl_id.seller_ids:
                    supp_id = supplierinfo.name.id
                    res[product.ean13]['seller_ids'][supp_id] = {}
                    for field in supplierinfo_fields:
                        res[product.ean13]['seller_ids'][supp_id][field] = {
                            'value': getattr(supplierinfo, field),
                            'field_name': _get_field_name(
                                self, cr, uid, field, 'product.supplierinfo')
                        }
        return res
