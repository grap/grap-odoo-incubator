# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    # Columns section
    valuation = fields.Float(
        string='Valuation', compute='_compute_valuation', store=True,
        digits_compute=dp.get_precision('Product Price'))

    # Compute Section
    @api.multi
    @api.depends('line_ids.valuation')
    def _compute_valuation(self):
        for inventory in self:
            inventory.valuation = sum(inventory.mapped('line_ids.valuation'))
