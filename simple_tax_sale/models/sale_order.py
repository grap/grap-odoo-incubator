# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api

from openerp.addons.simple_tax_account.models.res_partner\
    import SIMPLE_TAX_TYPE_KEYS


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    simple_tax_type = fields.Selection(
        related='partner_id.simple_tax_type', type='selection',
        selection=SIMPLE_TAX_TYPE_KEYS, string='Tax Type', readonly=True)

    @api.multi
    def recompute_simple_tax(self):
        tax_obj = self.env['account.tax']
        for order in self:
            for order_line in order.order_line:
                info = tax_obj._translate_simple_tax(
                    order.partner_id, order_line.price_unit,
                    order_line.tax_id)
                if (set(info['tax_ids']) !=
                        set([x.id for x in order_line.tax_id]) or
                        order_line.price_unit != info['price_unit']):
                    order_line.write({
                        'price_unit': info['price_unit'],
                        'tax_id': [(6, 0, info['tax_ids'])],
                    })
