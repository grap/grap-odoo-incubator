# -*- encoding: utf-8 -*-
##############################################################################
#
#    Mail - Send BCC for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

from openerp.osv.orm import Model
from openerp.osv import fields


class product_category(Model):
    _inherit = 'product.category'

    # Field Functions Section
    def _get_product_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for pc in self.browse(cr, uid, ids, context):
            res[pc.id] = len(pc.product_ids)
        return res

    # Columns Section
    _columns = {
        'product_ids': fields.one2many(
            'product.product', 'categ_id', 'Products', readonly=True),
        'product_qty': fields.function(
            _get_product_qty, type='integer', string='Products Quantity'),
    }
