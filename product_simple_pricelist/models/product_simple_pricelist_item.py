# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models, tools
from openerp.exceptions import Warning as UserError
from openerp.addons import decimal_precision as dp


class ProductSimplePricelistItem(models.Model):
    _name = 'product.simple.pricelist.item'
    _table = 'product_simple_pricelist_item'
    _auto = False

    _STATE_SELECTION = [
        ('set', 'Set'),
        ('not_set', 'Not Set'),
    ]

    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist', string='Pricelist', readonly=True)

    pricelist_version_id = fields.Many2one(
        comodel_name='product.pricelist.version', string='Pricelist Version',
        readonly=True)

    pricelist_item_id = fields.Many2one(
        comodel_name='product.pricelist.item', string='Pricelist Item',
        readonly=True)

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product', readonly=True)

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', readonly=True)

    specific_price = fields.Float(
        string='Specific Price', readonly=True,
        digits_compute=dp.get_precision('Product Price'))

    standard_price = fields.Float(
        string='Standard Price', readonly=True, _prefetch=False,
        digits_compute=dp.get_precision('Purchase Price'))

    list_price = fields.Float(
        string='List Price', readonly=True,
        digits_compute=dp.get_precision('Product Price'))

    state = fields.Selection(selection=_STATE_SELECTION, string='State')

    price = fields.Float(
        string='Price', compute='_compute_price',
        digits_compute=dp.get_precision('Product Price'))

    difference = fields.Float(string='Difference', readonly=True)

    product_active = fields.Boolean('Product Active')

    product_sale_ok = fields.Boolean('Product Can be sold')

    # Compute Section
    @api.depends('specific_price')
    def _compute_price(self):
        for item in self:
            item.price = item.specific_price or item.list_price

    # Custom Section
    @api.model
    def _get_product_id(self, str_id):
        return int(str_id[:9])

    @api.model
    def _get_pricelist_version_id(self, str_id):
        return int(str_id[9:])

    # View Section
    @api.multi
    def set_price_wizard(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        item_id = self.ids[0]
        ctx.update({
            'pricelist_version_id': self._get_pricelist_version_id(item_id),
            'product_id': self._get_product_id(item_id),
        })
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.simple.pricelist.item.update.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx,
        }

    @api.multi
    def remove_price(self):
        return self.mapped('pricelist_item_id').unlink()

    # Overload Section
    @api.multi
    def unlink(self):
        raise UserError(_(
            "Please unlink specific price by using according button."))
        # false super call, to avoid pylint error
        return super(ProductSimplePricelistItem, self).unlink()

    # Init Section
    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
            SELECT
                to_char(pp.id, 'FM099999999')
                    || to_char(pplv.id, 'FM099999999') AS id,
                pt.company_id AS company_id,
                pt.name AS product_name,
                pt.sale_ok AS product_sale_ok,
                pp.active AS product_active,
                pp.id AS product_id,
                pt.list_price,
                ppl.name,
                ppl.id as pricelist_id,
                pplv.id as pricelist_version_id,
                ppli.id as pricelist_item_id,
                ppli.price_surcharge as specific_price,
                CASE WHEN ppli.id is null
                    THEN 'not_set'
                    ELSE 'set'
                    END as state,
                CASE WHEN (ppli.id is null or pt.list_price = 0)
                    THEN 0
                    ELSE (ppli.price_surcharge - pt.list_price) / pt.list_price
                    END as difference
            FROM product_product pp
            INNER JOIN product_template pt
                ON pp.product_tmpl_id = pt.id
            JOIN product_pricelist ppl
                ON ppl.company_id = pt.company_id
                AND ppl.is_simple = True
            LEFT OUTER JOIN product_pricelist_version pplv
                ON pplv.pricelist_id = ppl.id
            LEFT OUTER JOIN product_pricelist_item ppli
                ON ppli.product_id = pp.id
                AND ppli.price_version_id = pplv.id
            WHERE
                (pp.active IS True AND pt.sale_ok IS True)
                OR ppli.id IS NOT null
        )""" % (self._table))
