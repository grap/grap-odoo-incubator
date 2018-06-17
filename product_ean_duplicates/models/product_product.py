# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError
from openerp.exceptions import Warning as UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Column Section
    ean13 = fields.Char(copy=False)

    ean_duplicates_exist = fields.Boolean(
        compute='_compute_ean_duplicates',
        string='Has EAN Duplicates', multi='ean_duplicates',
        search='_search_ean_duplicates_exist')

    ean_duplicates_qty = fields.Integer(
        compute='_compute_ean_duplicates',
        string='EAN Duplicates Quantity', multi='ean_duplicates')

    # Compute Section
    @api.multi
    def _compute_ean_duplicates(self):
        res = self._get_ean_duplicates()
        for product in self:
            if product.id in res:
                product.ean_duplicates_qty = res[product.id]
                product.ean_duplicates_exist = True

    # Search Section
    def _search_ean_duplicates_exist(self, operator, operand):
        products = self.search([])
        res = products._get_ean_duplicates()
        if operator == '=' and operand is True:
            product_ids = res.keys()
        elif operator == '=' and operand is False:
            product_ids = list(set(products.ids) - set(res.keys()))
        else:
            raise UserError(_(
                "Operator '%s' not implemented.") % (operator))
        return [('id', 'in', product_ids)]

    # Constrains Section
    @api.constrains('company_id', 'ean13')
    def _check_ean13_company(self):
        for product in self.search([('ean13', '!=', False)]):
            duplicates = self.with_context(active_test=True).search([
                ('company_id', '=', product.company_id.id),
                ('ean13', '=', product.ean13),
                ('id', '!=', product.id)])
            if duplicates:
                raise ValidationError(_(
                    "You can not set the ean13 '%s' for the product %s"
                    " because you have other products with the same"
                    " ean13 :\n - %s") % (
                        product.ean13, product.name,
                        '- %s\n'.join([x.name for x in duplicates])))

    # Private Section
    @api.multi
    def _get_ean_duplicates(self):
        self._cr.execute("""
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
            ORDER BY pp1.id""",
            (tuple(self.ids),))
        return {x[0]: x[1] for x in self._cr.fetchall()}
