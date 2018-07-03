# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    @api.model
    def create(self, vals):
        return super(StockInventoryLine, self.with_context(
            do_not_check_duplicates=True)).create(vals)

    @api.model
    def search(self, domain, *args, **kwargs):
        if self.env.context.get('do_not_check_duplicates', False):
            domain = [('product_id', '=', False)]
        return super(StockInventoryLine, self).search(domain, *args, **kwargs)
