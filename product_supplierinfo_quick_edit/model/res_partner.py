# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Simple Pricelist module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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


from openerp.osv import fields
from openerp.osv.orm import Model


class res_partner(Model):
    _inherit = 'res.partner'

    # Function Fields Section
    def _get_template_info(self, cr, uid, ids, name, args, context=None):
        res = {}
        supplierinfo_obj = self.pool['product.supplierinfo']
        for partner in self.browse(cr, uid, ids, context=context):
            supplierinfo_ids = supplierinfo_obj.search(cr, uid, [
                ('name', '=', partner.id)], context=context)
            supplierinfos = supplierinfo_obj.browse(
                cr, uid, supplierinfo_ids, context=context)
            template_ids = [x. product_tmpl_id for x in supplierinfos]
            res[partner.id] = {
                'template_ids': template_ids,
                'template_count': len(template_ids)}
        return res

    def _product_supplierinfo_2_res_partner(
            self, cr, uid, ids, context=None):
        """Return 'product.supplierinfo' Info
        where somes 'pricelist.partnerinfo' changes."""
        supplierinfo_obj = self.pool['product.supplierinfo']
        supplierinfos = supplierinfo_obj.browse(cr, uid, ids, context=context)
        res = [x.name.id for x in supplierinfos]
        return res

    # Column Section
    _columns = {
        'template_ids': fields.function(
            _get_template_info, type='one2many', relation='product.template',
            string='Products', multi='template_info', readonly=True),
        'template_count': fields.function(
            _get_template_info, type='integer', string='Products Quantity',
            multi='product_info', store={
                'product.supplierinfo': (
                    _product_supplierinfo_2_res_partner, [
                        'name',
                    ], 10)
                }),
    }
