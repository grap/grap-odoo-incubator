# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - EAN Duplicates Module for Odoo
#    Copyright (C) 2014 -Today GRAP (http://www.grap.coop)
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

from openerp import fields, models, api, _
from openerp.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _search_ean_duplicates_exist(self, operator, operand):
        products = self.search([])
        res = products._get_ean_duplicates()
        if operator == '=' and operand is True:
            product_ids = res.keys()
        elif operator == '=' and operand is False:
            product_ids = list(set(products.ids) - set(res.keys()))
        else:
            raise ValidationError(_(
                "Operator '%s' not implemented.") % (operator))
        return [('id', 'in', product_ids)]

    # Compute Section
    @api.multi
    def _get_ean_duplicates(self):
        sql_req = """
            SELECT
                pp1.id,
                count(*) as qty
            FROM product_product pp1
            INNER JOIN product_template pt1
                ON pt1.id = pp1.product_tmpl_id
            INNER JOIN product_product pp2
                ON pp1.ean13 = pp2.ean13
                AND pp1.id != pp2.id
                AND pp2.active = True
            INNER JOIN product_template pt2
                ON pt2.id = pp2.product_tmpl_id
                AND pt1.company_id = pt2.company_id
            WHERE
                pp1.ean13 IS NOT NULL
                AND pp1.ean13 != ''
                AND pp1.id in (%s)
            GROUP BY pp1.id
            ORDER BY pp1.id""" % (', '.join([str(id) for id in self.ids]))
        self._cr.execute(sql_req)  # pylint: disable=invalid-commit
        return {x[0]: x[1] for x in self._cr.fetchall()}

    @api.multi
    def _compute_ean_duplicates(self):
        res = self._get_ean_duplicates()
        for product in self:
            if product.id in res:
                product.ean_duplicates_qty = res[product.id]
                product.ean_duplicates_exist = True

    # Column Section
    ean13 = fields.Char(copy=False)
    ean_duplicates_exist = fields.Boolean(
        compute='_compute_ean_duplicates',
        string='Has EAN Duplicates', multi=_get_ean_duplicates,
        search=_search_ean_duplicates_exist)
    ean_duplicates_qty = fields.Integer(
        compute='_compute_ean_duplicates',
        string='EAN Duplicates Quantity', multi=_get_ean_duplicates)
