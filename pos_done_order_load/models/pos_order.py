# -*- coding: utf-8 -*-
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


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
            'amount_total', 'session_id',
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

    @api.multi
    def _prepare_done_order_for_pos(self):
        self.ensure_one()
        order_lines = []
        payment_lines = []
        for order_line in self.lines:
            order_line = self._prepare_done_order_line_for_pos(order_line)
            order_lines.append(order_line)
        for payment_line in self.statement_ids:
            payment_line = self._prepare_done_order_payment_for_pos(
                payment_line)
            payment_lines.append(payment_line)
        return {
            'id': self.id,
            'pos_reference': self.pos_reference,
            'name': self.name,
            'partner_id': self.partner_id.id,
            'line_ids': order_lines,
            'statement_ids': payment_lines,
        }

    @api.multi
    def _prepare_done_order_line_for_pos(self, order_line):
        self.ensure_one()
        return {
            'product_id': order_line.product_id.id,
            'qty': order_line.qty,
            'price_unit': order_line.price_unit,
            'discount': order_line.discount,
        }

    @api.multi
    def _prepare_done_order_payment_for_pos(self, payment_line):
        self.ensure_one()
        return {
            'statement_id': payment_line.statement_id.id,
            'amount': payment_line.amount,
        }

    @api.multi
    def load_done_order_for_pos(self):
        self.ensure_one()
        return self._prepare_done_order_for_pos()
