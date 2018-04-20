# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False):
        partner_obj = self.env['res.partner']
        tax_obj = self.env['account.tax']

        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=True,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)

        if res['value'].get('price_unit', False) and\
                res['value'].get('tax_id', False):
            partner = partner_obj.browse(partner_id)
            taxes = tax_obj.browse(res['value']['tax_id'])
            info = tax_obj._translate_simple_tax(
                partner, res['value']['price_unit'], taxes)
            res['value'].update({
                'price_unit': info['price_unit'],
                'tax_id': info['tax_ids'],
            })
        return res
