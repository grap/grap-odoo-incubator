# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from openerp.osv.orm import setup_modifiers
from openerp.osv.orm import Model


class ProductProduct(Model):
    _inherit = 'product.product'

    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False, submenu=False):
        if context is None:
            context = {}
        res = super(ProductProduct, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=False)
        if view_type in ('form', 'tree'):
            doc = etree.XML(res['arch'])
            nodes = doc.xpath("//field[@name='tax_group_id']")
            if nodes:
                nodes[0].set('required', '1')
                setup_modifiers(nodes[0], res['fields']['tax_group_id'])
                res['arch'] = etree.tostring(doc)
        return res
