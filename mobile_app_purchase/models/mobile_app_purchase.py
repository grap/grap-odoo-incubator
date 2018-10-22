# coding: utf-8
# Copyright (C) 2016 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, models


class MobileAppPurchase(models.TransientModel):
    _name = 'mobile.app.purchase'

    # Public API Section
    @api.model
    def check_group(self, group_ext_id):
        return self.env.user.has_group(group_ext_id)

    @api.model
    def create_order_by_scan(self, partner_id):
        vals = self.default_get(self._defaults.keys())

        # Set Supplier
        vals.update({'partner_id': partner_id})
        vals.update(self.onchange_partner_id(partner_id)['value'])

        # Get Picking Type
        vals['picking_type_id'] = self._get_picking_in()
        vals['location_id'] = self.onchange_picking_type_id(
            vals['picking_type_id'])['value']['location_id']

        vals['origin'] = _("Barcode Reader")
        return super(MobileAppPurchase, self).create(vals).id

    @api.model
    def add_order_line(self, order_id, product_id, qty):
        line_obj = self.env['purchase.order.line']

        # Secure type before calling onchange_product_id func that doesn't
        # work with str value
        qty = float(qty)

        order = self.browse(order_id)
        uom_id = False
        pricelist_id = order.pricelist_id.id
        partner_id = order.partner_id.id
        line_vals = line_obj.onchange_product_id(
            pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=order.date_order,
            fiscal_position_id=order.fiscal_position.id,
            date_planned=order.minimum_planned_date, name=False,
            price_unit=False)['value']
        line_vals.update({
            'product_id': product_id,
            'order_id': order.id,
        })
        # This framework is awsome
        line_vals['taxes_id'] = [[6, False, line_vals['taxes_id']]]
        order_vals = {'order_line': [[0, False, line_vals]]}
        return order.write(order_vals)




    # _SCAN_TO_PURCHASE_MANDATORY_FIELDS = ['id', 'name', 'ean13']

    # def _scan_to_purchase_product_fields(self, cr, uid, context=None):
    #     user_obj = self.pool['res.users']
    #     company = user_obj.browse(cr, uid, uid, context=context).company_id
    #     return [x.name for x in company.scan_purchase_product_fields_ids]

    # def _scan_to_purchase_supplierinfo_fields(self, cr, uid, context=None):
    #     user_obj = self.pool['res.users']
    #     company = user_obj.browse(cr, uid, uid, context=context).company_id
    #     return [x.name for x in company.scan_purchase_supplierinfo_fields_ids]

    @api.model
    def get_products(self, cr, uid, context=None):
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
