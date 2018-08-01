# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    # Columns Section
    template_qty = fields.Integer(
        compute='_compute_multi_qty', string='Products Quantity')

    product_qty = fields.Integer(
        compute='_compute_multi_qty', string='Variants Quantity')

    # Compute Section
    @api.multi
    def _compute_multi_qty(self):
        res = {}
        search = self.env['product.template'].read_group(
            [], ['categ_id'], ['categ_id'])
        for item in search:
            res[item['categ_id'][0]] = item['categ_id_count']
        for category in self:
            category.template_qty = res.get(category.id, 0)

        res = {}
        search = self.env['product.product'].read_group(
            [], ['categ_id'], ['categ_id'])
        for item in search:
            res[item['categ_id'][0]] = item['categ_id_count']
        for category in self:
            category.product_qty = res.get(category.id, 0)
