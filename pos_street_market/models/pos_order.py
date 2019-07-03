# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # Columns section
    market_place_id = fields.Many2one(
        string='Market Place', comodel_name='market.place')

    # Overload 'date_order' column to make readonly to false
    date_order = fields.Datetime(readonly=False)

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['market_place_id'] = ui_order.get('market_place_id', False)
        return res
