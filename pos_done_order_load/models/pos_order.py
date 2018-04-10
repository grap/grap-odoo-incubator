# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # Custom Section
    @api.model
    def _prepare_filter_for_pos(self, pos_session_id):
        return [
            ('state', 'in', ['paid', 'done', 'invoiced']),
        ]


    @api.model
    def _prepare_filter_query_for_pos(self, pos_session_id, query):
        return [
            '|',
            ('name', 'ilike', query),
            ('pos_reference', 'ilike', query),
        ]

    @api.model
    def _prepare_fields_for_pos_list(self):
        return [
            'name', 'pos_reference', 'partner_id', 'date_order',
            'amount_total',
        ]

    @api.model
    def search_done_orders_for_pos(self, query, pos_session_id):
        session_obj = self.env['pos.session']
        config = session_obj.browse(pos_session_id).config_id
        condition = self._prepare_filter_for_pos(pos_session_id) +\
            self._prepare_filter_query_for_pos(pos_session_id, query)
        fields = self._prepare_fields_for_pos_list()
        return self.search_read(
            condition, fields, limit=config.iface_load_done_order_max_qty)

#    @api.multi
#    def load_picking_for_pos(self):
#        self.ensure_one()
#        pickinglines = []
#        for line in self.move_lines.filtered(lambda x: x.state != 'cancel'):
#            picking_line = {
#                'name': line.name,
#                'product_id': line.product_id.id,
#                'quantity': line.product_uom_qty,
#            }
#            sale_order_line =\
#                line.procurement_id and line.procurement_id.sale_line_id
#            if sale_order_line:
#                # Get price and discount of the order if available
#                picking_line['price_unit'] = sale_order_line.price_unit
#                picking_line['discount'] = sale_order_line.discount
#            pickinglines.append(picking_line)
#        return {
#            'id': self.id,
#            'name': self.name,
#            'partner_id': self.partner_id.id,
#            'line_ids': pickinglines,
#        }

