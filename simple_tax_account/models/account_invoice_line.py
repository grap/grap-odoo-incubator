# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def product_id_change(
            self, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None):
        partner_obj = self.env['res.partner']
        tax_obj = self.env['account.tax']

        res = super(AccountInvoiceLine, self).product_id_change(
            product, uom_id, qty=qty, name=name, type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit, currency_id=currency_id,
            company_id=company_id)

        if res['value'].get('price_unit', False):
            partner = partner_obj.browse(partner_id)
            taxes = tax_obj.browse(res['value']['invoice_line_tax_id'])
            info = tax_obj._translate_simple_tax(
                partner, res['value']['price_unit'], taxes)
            res['value'].update({
                'price_unit': info['price_unit'],
                'invoice_line_tax_id': info['tax_ids'],
            })

        return res
