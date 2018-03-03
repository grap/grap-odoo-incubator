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
from openerp.osv.osv import except_osv
from openerp.tools.translate import _
from openerp.addons import decimal_precision as dp


class product_supplierinfo(Model):
    _inherit = 'product.supplierinfo'

    # Function Fields Section
    def _get_simple_info(self, cr, uid, ids, name, args, context=None):
        res = {}

        for item in self.browse(cr, uid, ids, context=context):
            if len(item.pricelist_ids) == 1:
                res[item.id] = {
                    'simple_min_quantity': item.pricelist_ids[0].min_quantity,
                    'simple_price': item.pricelist_ids[0].price,
                    'simple_discount': item.pricelist_ids[0].discount,
                }
            else:
                res[item.id] = {
                    'simple_min_quantity': 0,
                    'simple_price': 0,
                    'simple_discount': 0,
                }
            res[item.id]['template_standard_price'] =\
                item.product_tmpl_id and\
                item.product_tmpl_id.standard_price or 0
            res[item.id]['template_cost_method'] =\
                item.product_tmpl_id and item.product_tmpl_id.cost_method or ''
        return res

    def _get_lines_qty(self, cr, uid, ids, name, args, context=None):
        res = {}
        for item in self.browse(cr, uid, ids, context=context):
            res[item.id] = len(item.pricelist_ids)
        return res

    def _set_simple_min_quantity(
            self, cr, uid, id, name, value, args, context=None):
        partnerinfo_obj = self.pool['pricelist.partnerinfo']
        supplierinfo = self.browse(cr, uid, id, context=context)
        if len(supplierinfo.pricelist_ids) == 1:
            return partnerinfo_obj.write(
                cr, uid, supplierinfo.pricelist_ids[0].id,
                {'min_quantity': value}, context=context)
        else:
            return True

    def _set_simple_price(
            self, cr, uid, id, name, value, args, context=None):
        partnerinfo_obj = self.pool['pricelist.partnerinfo']
        supplierinfo = self.browse(cr, uid, id, context=context)
        if len(supplierinfo.pricelist_ids) == 1:
            return partnerinfo_obj.write(
                cr, uid, supplierinfo.pricelist_ids[0].id,
                {'price': value}, context=context)
        else:
            return True

    def _set_simple_discount(
            self, cr, uid, id, name, value, args, context=None):
        partnerinfo_obj = self.pool['pricelist.partnerinfo']
        supplierinfo = self.browse(cr, uid, id, context=context)
        if len(supplierinfo.pricelist_ids) == 1:
            return partnerinfo_obj.write(
                cr, uid, supplierinfo.pricelist_ids[0].id,
                {'discount': value}, context=context)
        else:
            return True

    def _get_product_supplierinfo_pricelist_partnerinfo(
            self, cr, uid, ids, context=None):
        """Return 'product.supplierinfo' Info
        where somes 'pricelist.partnerinfo' changes."""
        partnerinfo_obj = self.pool['pricelist.partnerinfo']
        partnerinfos = partnerinfo_obj.browse(cr, uid, ids, context=context)
        res = [x.suppinfo_id.id for x in partnerinfos]
        return res

    # Column Section
    _columns = {
        'template_cost_method': fields.function(
            _get_simple_info, type='char',
            string='Cost', multi='simple_info', readonly=True),
        'template_standard_price': fields.function(
            _get_simple_info,
            type='float', string='Cost', multi='simple_info', required=True,
            digits_compute=dp.get_precision('Purchase Price')),
        'simple_min_quantity': fields.function(
            _get_simple_info, fnct_inv=_set_simple_min_quantity, type='float',
            string='Simple Minimum Quantity', multi='simple_info',
            required=True),
        'simple_price': fields.function(
            _get_simple_info, fnct_inv=_set_simple_price, type='float',
            string='Simple Price', multi='simple_info', required=True,
            digits_compute=dp.get_precision('Purchase Price')),
        'simple_discount': fields.function(
            _get_simple_info, fnct_inv=_set_simple_discount, type='float',
            string='Simple Discount', multi='simple_info', required=True,
            digits=(16, 2)),
        'lines_qty': fields.function(
            _get_lines_qty, type='integer', string='Lines Quantity',
            store={
                'product.supplierinfo': (
                    lambda self, cr, uid, ids, context=None: ids, [
                        'pricelist_ids', 'name',
                    ], 10),
                'pricelist.partnerinfo': (
                    _get_product_supplierinfo_pricelist_partnerinfo, [
                        'suppinfo_id',
                    ], 10)
                }),
    }

    # Custom Section
    def create_simple_line(self, cr, uid, ids, context=None):
        partnerinfo_obj = self.pool['pricelist.partnerinfo']
        vals = {'min_quantity': 0, 'price': 0}
        defaults = partnerinfo_obj._add_missing_default_values(cr, uid, {})
        vals.update(defaults)
        for item in self.browse(cr, uid, ids, context=context):
            if len(item.pricelist_ids) == 0:
                vals['suppinfo_id'] = item.id
                partnerinfo_obj.create(cr, uid, vals, context=context)
            else:
                # This case occures in the case of concurrent access
                lines = ';\n - '.join([_(
                    'qty : %s - price : %s') % (x.min_quantity, x.price)
                    for x in item.pricelist_ids])
                raise except_osv(_('Error!'), _(
                    "You can not create a simple supplier line for '%s'"
                    " product because it has already one (or many)"
                    " lines.\n\n - %s" % (item.product_tmpl_id.name, lines)))
        return True

    def edit_multiple_lines(self, cr, uid, ids, context=None):
        assert (len(ids) == 1)
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.supplierinfo',
            'type': 'ir.actions.act_window',
            'res_id': ids[0],
            'target': 'new',
            'context': context,
            'nodestroy': True,
        }
