# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def onchange_product_id(
            self, pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=False, fiscal_position_id=False,
            date_planned=False, name=False, price_unit=False, state='draft'):
        partner_obj = self.env['res.partner']
        tax_obj = self.env['account.tax']

        res = super(PurchaseOrderLine, self).onchange_product_id(
            pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=date_order, fiscal_position_id=fiscal_position_id,
            date_planned=date_planned, name=name, price_unit=price_unit,
            state=state)

        if res['value'].get('price_unit', False) and\
                res['value'].get('taxes_id', False):
            partner = partner_obj.browse(partner_id)
            taxes = tax_obj.browse(res['value']['taxes_id'])
            info = tax_obj._translate_simple_tax(
                partner, res['value']['price_unit'], taxes)
            res['value'].update({
                'price_unit': info['price_unit'],
                'taxes_id': info['tax_ids'],
            })
        return res
