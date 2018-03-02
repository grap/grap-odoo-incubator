# -*- coding: utf-8 -*-
# Copyright (c) 2016 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                    Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#                    Andrius Preimantas <andrius@versada.lt>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.model
    def _get_po_line_values_from_proc(
            self, procurement, partner, company, schedule_date):
        # Include discount in Purchase Order Line created from procurement
        order_line_obj = self.env['purchase.order.line']
        res = super(ProcurementOrder, self)._get_po_line_values_from_proc(
            procurement, partner, company, schedule_date)
        supplierinfo = order_line_obj._get_product_supplierinfo_discount(
            procurement.product_id.id, res['product_qty'], partner.id)
        if supplierinfo:
            res['discount2'] = supplierinfo.discount2
            res['discount3'] = supplierinfo.discount3
        return res
