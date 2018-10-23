# coding: utf-8
# Copyright (C) 2016 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, models


class MobileAppPurchase(models.TransientModel):
    _name = 'mobile.app.purchase'

    _MANDATORY_FIELDS = ['id', 'name', 'ean13']

    # Public API Section - Generic Functions
    @api.model
    def check_group(self, group_ext_id):
        return self.env.user.has_group(group_ext_id)

    # Public API Section - Load Functions
    @api.model
    def get_purchase_orders(self):
        """Return purchase orders available for the Mobile App
        :return: [purchase_order_1_vals, purchase_order_2_vals, ...]
        .. seealso:: _export_purchase_order() for purchase order vals details.
        """
        PurchaseOrder = self.env['purchase.order']
        orders = PurchaseOrder.search(self._get_purchase_order_domain())
        return [
            self._export_purchase_order(order) for order in orders]

    @api.model
    def get_partners(self, params):
        """ Return supplier partners.
        :param params: no params.
        :return: [partner_1_vals, partner_2_vals, ...]
        .. seealso::
            _export_partner() for partner vals details
        """
        ResPartner = self.env['res.partner']
        partners = ResPartner.search(self._get_partner_domain())
        return [
            self._export_partner(partner) for partner in partners]

    @api.model
    def create_purchase_order(self, params):
        """Create a new purchase order.
        :param params: {'partner': partner_vals}
        :return: purchase_order_vals_vals
        .. seealso::
            _export_purchase_order() for purchase order vals details
        """
        PurchaseOrder = self.env['purchase.order']
        partner_id = self._extract_param(params, 'partner.id')
        vals = PurchaseOrder.default_get(PurchaseOrder._defaults.keys())

        # Set Supplier
        vals.update({'partner_id': partner_id})
        vals.update(PurchaseOrder.onchange_partner_id(partner_id)['value'])

        # Get Picking Type
        vals['picking_type_id'] = PurchaseOrder._get_picking_in()
        vals['location_id'] = PurchaseOrder.onchange_picking_type_id(
            vals['picking_type_id'])['value']['location_id']

        vals['origin'] = _("Barcode Reader")
        order = PurchaseOrder.create(vals)
        return self._export_purchase_order(order)

    @api.model
    def add_purchase_order_line(self, params):
        order_id = self._extract_param(params, 'purchase_order.id')
        product_id = self._extract_param(params, 'product.id')
        qty = self._extract_param(params, 'qty')

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
        res = order.write(order_vals)
        return res

    @api.model
    def get_products(self, params):
        """ Return products of a given purchase order.
        :param params: {'purchase_order': purchase_order_vals}
        :return: [product_1_vals, product_2_vals, ...]
        .. seealso::
            _export_product() for product vals details
        """
        ResPartner = self.env['res.partner']
        partner_id = self._extract_param(params, 'purchase_order.partner.id')
        partner = ResPartner.browse(partner_id)
        ProductSupplierinfo = self.env['product.supplierinfo']
        supplierinfos = ProductSupplierinfo.search([
            ('name', '=', partner.id)])
        products = supplierinfos.mapped('product_tmpl_id.product_variant_ids')

        custom_fields = self._get_custom_fields()
        supplier_fields = self._get_supplier_fields()

        return [
            self._export_product(
                product, partner, custom_fields,
                supplier_fields) for product in products]

    @api.model
    def search_barcode(self, params):
        barcode = self._extract_param(params, 'barcode')

        product_obj = self.env['product.product']
        products = product_obj.search([('ean13', '=', barcode)])
        if not products:
            return False
        else:
            custom_fields = self._get_custom_fields()
            supplier_fields = self._get_supplier_fields()

            return self._export_product(
                products[0], False, custom_fields,
                supplier_fields)

    @api.model
    def _export_product(
            self, product, partner, custom_fields, supplier_fields):
        # Custom product fields
        custom_vals = {}
        supplier_vals = {}
        for field_name, field_display in custom_fields.iteritems():
            if field_name[-3:] == '_id':
                value = getattr(product, field_name).name
            elif field_name[-4:] == '_ids':
                value = ", ".join(
                    [attr.name for attr in getattr(product, field_name)])
            else:
                value = getattr(product, field_name)
            custom_vals[field_display] = value

        return {
            'id': product.id,
            'name': product.name,
            'barcode': product.ean13,
            'custom_vals': custom_vals,
            'supplier_vals': supplier_vals,
        }

    # @api.model
    # def get_products(self):
    #     def _get_field_display(obj, field_name):
    #         translation_obj = obj.env['ir.translation']
    #         # Determine model name
    #         if field_name in obj.env['product.product']._columns:
    #             model = 'product.product'
    #         elif field_name in obj.env['product.template']._columns:
    #             model = 'product.template'
    #         else:
    #             model = 'product.supplierinfo'
    #         # Get translation if defined
    #         translation_ids = translation_obj.search([
    #             ('lang', '=', obj.env.context.get('lang', False)),
    #             ('type', '=', 'field'),
    #             ('name', '=', '%s,%s' % (model, field_name))])
    #         if translation_ids:
    #             return translation_ids[0].value
    #         else:
    #             return obj.env[model]._columns[field_name].string

    #     company = self.env.user.company_id
    #     product_fields = [
    #         x.name for x in company.mobile_purchase_product_field_ids]
    #     supplierinfo_fields = [
    #         x.name for x in company.mobile_purchase_supplierinfo_field_ids]

    #     ProductProduct = self.env['product.product']

    #     res = {}
    #     products = ProductProduct.search([('ean13', '!=', False)])
    #     for product in products:
    #         res[product.ean13] = {}
    #         # Add product fields
    #         for field in self._MANDATORY_FIELDS:
    #             res[product.ean13][field] = getattr(product, field)

    #         for field in product_fields:
    #             if field[-3:] == '_id':
    #                 res[product.ean13][field] = {
    #                     'id': getattr(product, field).id,
    #                     'value': getattr(product, field).name,
    #                     'field_name': _get_field_display(self, field),
    #                 }
    #             else:
    #                 res[product.ean13][field] = {
    #                     'value': getattr(product, field),
    #                     'field_name': _get_field_display(self, field),
    #                 }

    #         # Add supplierinfo fields
    #         res[product.ean13]['seller_ids'] = {}
    #         if supplierinfo_fields:
    #             for supplierinfo in product.product_tmpl_id.seller_ids:
    #                 supp_id = supplierinfo.name.id
    #                 res[product.ean13]['seller_ids'][supp_id] = {}
    #                 for field in supplierinfo_fields:
    #                     res[product.ean13]['seller_ids'][supp_id][field] = {
    #                         'value': getattr(supplierinfo, field),
    #                         'field_name': _get_field_display(self, field)
    #                     }
    #     return res

    # Private - Domain Section
    @api.model
    def _get_purchase_order_domain(self):
        return [('state', '=', 'draft')]

    @api.model
    def _get_partner_domain(self):
        return [('supplier', '=', True)]

    # Private - Export Section
    @api.model
    def _export_purchase_order(self, order):
        return {
            'id': order.id,
            'name': order.name,
            'partner': self._export_partner(order.partner_id),
            'amount_untaxed': order.amount_untaxed,
            'amount_total': order.amount_total,
            'minimum_planned_date': order.minimum_planned_date,
            'line_qty': len(order.order_line),
        }

    @api.model
    def _export_partner(self, partner):
        return {
            'id': partner.id,
            'name': partner.name,
            'city': partner.city,
            'purchase_order_count': partner.purchase_order_count,
        }

    # Private - Tools Section
    @api.model
    def _get_custom_fields(self):
        """Return a list of (field_name, field_display) for each custom
        product fields that should be displayed during the purchase.
        Don't work yet with computed fields (like display_name)
        """
        res = {}
        company = self.env.user.company_id
        for field in company.mobile_purchase_product_field_ids:
            res[field.name] = self._get_field_display(field)
        return res

    def _get_supplier_fields(self):
        """Return a list of (field_name, field_display) for each custom
        supplier info fields that should be displayed during the purchase.
        Don't work yet with computed fields (like display_name)
        """
        res = {}
        company = self.env.user.company_id
        for field in company.mobile_inventory_supplier_field_ids:
            res[field.name] = self._get_field_display(
                field, 'product.supplierinfo')
        return res

    @api.model
    def _get_field_display(self, field, model_name=False):
        IrTranslation = self.env['ir.translation']
        # Determine model name
        if not model_name:
            if field.name in self.env['product.product']._columns:
                model_name = 'product.product'
            else:
                model_name = 'product.template'
        # Get translation if defined
        translation_ids = IrTranslation.search([
            ('lang', '=', self.env.context.get('lang', False)),
            ('type', '=', 'field'),
            ('name', '=', '%s,%s' % (model_name, field.name))])
        if translation_ids:
            return translation_ids[0].value
        else:
            return self.env[model_name]._columns[field.name].string

    @api.model
    def _extract_param(self, params, value_path):
        if not type(params) is dict:
            return False
        if '.' in value_path:
            # Recursive call
            value_path_split = value_path.split('.')
            first_key = value_path_split[0]
            return self._extract_param(
                params.get(first_key),
                '.'.join(value_path_split[1:]))
        else:
            return params.get(value_path, False)
