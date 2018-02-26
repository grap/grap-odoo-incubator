# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api

from .res_partner import SIMPLE_TAX_TYPE_KEYS


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    simple_tax_type = fields.Selection(
        related='partner_id.simple_tax_type', string='Tax Type',
        readonly=True, selection=SIMPLE_TAX_TYPE_KEYS)

    @api.multi
    def recompute_simple_tax(self):
        tax_obj = self.env['account.tax']

        for invoice in self:
            for invoice_line in invoice.invoice_line:
                info = tax_obj._translate_simple_tax(
                    invoice.partner_id, invoice_line.price_unit,
                    invoice_line.invoice_line_tax_id)
                # Update only if necessary
                if (set(info['tax_ids']) != set(
                        [x.id for x in invoice_line.invoice_line_tax_id]) or
                        invoice_line.price_unit != info['price_unit']):
                    invoice_line.write({
                        'price_unit': info['price_unit'],
                        'invoice_line_tax_id': [(6, 0, info['tax_ids'])],
                    })
