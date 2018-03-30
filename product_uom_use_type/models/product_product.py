# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def onchange_uom(self, uom_id, uom_po_id):
        uom_obj = self.env['product.uom']
        res = super(ProductProduct, self).onchange_uom(uom_id, uom_po_id)
        if not res:
            return res
        value = res.setdefault('value', {})
        if value.get('uom_id', False):
            uom = uom_obj.browse(value.get('uom_id', False))
            if uom.use_type == 'purchase':
                value['uom_id'] = False
        if value.get('uom_po_id', False):
            uom_po = uom_obj.browse(value.get('uom_po_id', False))
            if uom_po.use_type == 'sale':
                value['uom_po_id'] = False
        return res
