# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Street Market module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields


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
