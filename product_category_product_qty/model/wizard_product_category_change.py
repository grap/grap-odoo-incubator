# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Category Improve for Odoo
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

from openerp.osv.orm import TransientModel
from openerp.osv import fields


class wizard_product_category_change(TransientModel):
    _name = 'wizard.product.category.change'

    def _get_default_categ_id_from(self, cr, uid, context=None):
        if context['active_model'] == 'product.category':
            return context['active_id']
        else:
            return False

    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False, submenu=False):
        result = super(wizard_product_category_change, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=submenu)

        if view_type == 'form':
            if context.get('active_model') == 'product.product':
                result['fields']['is_mass_change']['invisible'] = True
                result['fields']['categ_id_from']['invisible'] = True
            elif context.get('active_model') == 'product.category':
                result['fields']['categ_id_from']['required'] = True
        return result

    _columns = {
        'is_mass_change': fields.boolean(
            'Mass change'),
        'categ_id_from': fields.many2one(
            'product.category', 'Category Origin'),
        'categ_id_to': fields.many2one(
            'product.category', 'Category Destination', required=True,
            domain="""[('type', '=', 'normal'),
                ('id', '!=', categ_id_from)]"""),
    }

    _defaults = {
        'is_mass_change': (
            lambda self, cr, uid, ctx:
            ctx.get('active_model') == 'product.category'),
        'categ_id_from': _get_default_categ_id_from,
    }

    def change_category(self, cr, uid, ids, context=None):
        pp_obj = self.pool['product.product']
        assert len(ids) == 1
        wpcc = self.browse(cr, uid, ids[0], context=context)
        if wpcc.is_mass_change:
            # change of all products of a category
            pp_ids = [x.id for x in wpcc.categ_id_from.product_ids]
            pp_obj.write(
                cr, uid, pp_ids,
                {'categ_id': wpcc.categ_id_to.id})
        else:
            # Change on selected product
            pp_obj.write(
                cr, uid, context['active_ids'],
                {'categ_id': wpcc.categ_id_to.id})
        return True
