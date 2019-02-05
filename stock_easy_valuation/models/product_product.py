# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Compute Section
    @api.multi
    def _compute_valuation_qty_available(self):
        for product in self:
            product.valuation_qty_available =\
                product.qty_available * product.standard_price

    @api.multi
    def _compute_valuation_virtual_available(self):
        for product in self:
            product.valuation_virtual_available =\
                product.virtual_available * product.standard_price

    # Columns Section
    valuation_qty_available = fields.Float(
        compute='_compute_valuation_qty_available',
        string='Valuation of Quantity on Hand')
    valuation_virtual_available = fields.Float(
        compute='_compute_valuation_virtual_available',
        string='Valuation of Virtual Quantity')
