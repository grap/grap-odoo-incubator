# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

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
        return super(PurchaseOrder, self).create(vals).id

    @api.model
    def add_order_line_by_scan(self, order_id, product_id, qty):
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
