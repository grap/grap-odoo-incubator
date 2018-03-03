# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class ProductSupplierinfoCreatePurchaseOrder(models.TransientModel):
    _name = 'product.supplierinfo.create.purchase.order'

    purchase_disabled_products = fields.Boolean(
        string='Purchase Disabled Products', default=True)

    @api.multi
    def create_purchase_order(self):
        self.ensure_one()
        order_obj = self.env['purchase.order']
        line_obj = self.env['purchase.order.line']
        product_obj = self.env['product.product']
        supplierinfo_obj = self.env['product.supplierinfo']
        supplierinfos = supplierinfo_obj.browse(
            self.env.context.get('active_ids', []))

        # Create a dict of partner / product_ids
        create_data = {}
        for supplierinfo in supplierinfos:
            products = product_obj.with_context(
                active_test=not self.purchase_disabled_products).search(
                [('product_tmpl_id', '=', supplierinfo.product_tmpl_id.id)])
            if supplierinfo.name.id in create_data:
                create_data[supplierinfo.name.id] += products.ids
            else:
                create_data[supplierinfo.name.id] = products.ids

        # Create a Purchase order for each partner
        order_ids = []
        for partner_id, product_ids in create_data.iteritems():
            order_data = order_obj._add_missing_default_values({})
            order_data['partner_id'] = partner_id
            order_data.update(
                order_obj.onchange_partner_id(partner_id)['value'])

            # Get default stock location
            order_data['picking_type_id'] = order_obj._get_picking_in()
            order_data['location_id'] = order_obj.onchange_picking_type_id(
                order_data['picking_type_id'])['value']['location_id']

            order_data['order_line'] = []
            for product_id in product_ids:
                line_data = {'product_id': product_id}
                line_data.update(line_obj.onchange_product_id(
                    order_data['pricelist_id'], product_id, 1,
                    False, order_data['partner_id'],
                    fiscal_position_id=order_data['fiscal_position'])['value'])
                line_data['taxes_id'] = [
                    [6, False, line_data['taxes_id'] or []]]
                order_data['order_line'].append([0, False, line_data])

            order = order_obj.create(order_data)

            order_ids.append(str(order.id))

        res = {
            'domain': "[('id','in', [" + ','.join(order_ids) + "])]",
            'name': _('Purchase Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }
        return res
