# coding: utf-8
# Copyright (C) 2016 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, models


class MobileAppPurchase(models.TransientModel):
    _name = 'mobile.app.purchase'

    _MANDATORY_FIELDS = ['id', 'name', 'ean13']

    # Public API Section
    @api.model
    def check_group(self, group_ext_id):
        return self.env.user.has_group(group_ext_id)

    @api.model
    def create_purchase_order(self, partner_id):
        PurchaseOrder = self.env['purchase.order']
        vals = PurchaseOrder.default_get(PurchaseOrder._defaults.keys())

        # Set Supplier
        vals.update({'partner_id': partner_id})
        vals.update(PurchaseOrder.onchange_partner_id(partner_id)['value'])

        # Get Picking Type
        vals['picking_type_id'] = PurchaseOrder._get_picking_in()
        vals['location_id'] = PurchaseOrder.onchange_picking_type_id(
            vals['picking_type_id'])['value']['location_id']

        vals['origin'] = _("Barcode Reader")
        return PurchaseOrder.create(vals).id

    @api.model
    def add_purchase_order_line(self, order_id, product_id, qty):
        PurchaseOrder = self.env['purchase.order']

        PurchaseOrderLine = self.env['purchase.order.line']

        # Secure type before calling onchange_product_id func that doesn't
        # work with str value
        qty = float(qty)

        order = PurchaseOrder.browse(order_id)
        uom_id = False
        pricelist_id = order.pricelist_id.id
        partner_id = order.partner_id.id
        line_vals = PurchaseOrderLine.onchange_product_id(
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

    @api.model
    def get_products(self):
        def _get_field_display(obj, field_name):
            translation_obj = obj.env['ir.translation']
            # Determine model name
            if field_name in obj.env['product.product']._columns:
                model = 'product.product'
            elif field_name in obj.env['product.template']._columns:
                model = 'product.template'
            else:
                model = 'product.supplierinfo'
            # Get translation if defined
            translation_ids = translation_obj.search([
                ('lang', '=', obj.env.context.get('lang', False)),
                ('type', '=', 'field'),
                ('name', '=', '%s,%s' % (model, field_name))])
            if translation_ids:
                return translation_ids[0].value
            else:
                return obj.env[model]._columns[field_name].string

        company = self.env.user.company_id
        product_fields = [
            x.name for x in company.mobile_purchase_product_field_ids]
        supplierinfo_fields = [
            x.name for x in company.mobile_purchase_supplierinfo_field_ids]

        ProductProduct = self.env['product.product']

        res = {}
        products = ProductProduct.search([('ean13', '!=', False)])
        for product in products:
            res[product.ean13] = {}
            # Add product fields
            for field in self._MANDATORY_FIELDS:
                res[product.ean13][field] = getattr(product, field)

            for field in product_fields:
                if field[-3:] == '_id':
                    res[product.ean13][field] = {
                        'id': getattr(product, field).id,
                        'value': getattr(product, field).name,
                        'field_name': _get_field_display(self, field),
                    }
                else:
                    res[product.ean13][field] = {
                        'value': getattr(product, field),
                        'field_name': _get_field_display(self, field),
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
                            'field_name': _get_field_display(self, field)
                        }
        return res
