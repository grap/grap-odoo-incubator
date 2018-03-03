# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError

from openerp.addons import decimal_precision as dp


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    # Column Section
    template_standard_price = fields.Float(
        related='product_tmpl_id.standard_price', string='Cost',
        digits_compute=dp.get_precision('Purchase Price'))

    simple_min_quantity = fields.Float(
        compute='_get_simple_info', inverse='_set_simple_min_quantity',
        string='Simple Minimum Quantity', multi='simple_info',
        required=True)

    simple_price = fields.Float(
        compute='_get_simple_info', inverse='_set_simple_price',
        string='Simple Price', multi='simple_info', required=True,
        digits_compute=dp.get_precision('Purchase Price'))

    simple_discount = fields.Float(
        compute='_get_simple_info', inverse='_set_simple_discount',
        string='Simple Discount (%)', multi='simple_info', required=True,
        digits_compute=dp.get_precision('Discount'))

    simple_discount2 = fields.Float(
        compute='_get_simple_info', inverse='_set_simple_discount2',
        string='Simple Discount 2 (%)', multi='simple_info', required=True,
        digits_compute=dp.get_precision('Discount'))

    simple_discount3 = fields.Float(
        compute='_get_simple_info', inverse='_set_simple_discount3',
        string='Simple Discount 3 (%)', multi='simple_info', required=True,
        digits_compute=dp.get_precision('Discount'))

    lines_qty = fields.Integer(
        compute='_get_lines_qty', string='Lines Quantity', store=True)

    # Compute Section
    @api.multi
    @api.depends('product_tmpl_id.standard_price')
    def _get_simple_info(self):
        for item in self:
            if len(item.pricelist_ids) == 1:
                item.write({
                    'simple_min_quantity': item.pricelist_ids[0].min_quantity,
                    'simple_price': item.pricelist_ids[0].price,
                    'simple_discount': item.pricelist_ids[0].discount,
                    'simple_discount2': item.pricelist_ids[0].discount2,
                    'simple_discount3': item.pricelist_ids[0].discount3,
                })

    @api.multi
    @api.depends('pricelist_ids')
    def _get_lines_qty(self):
        for item in self:
            item.lines_qty = len(item.pricelist_ids)

    @api.multi
    def _set_simple_min_quantity(self):
        self.ensure_one()
        if len(self.pricelist_ids) == 1:
            self.pricelist_ids[0].min_quantity = self.simple_min_quantity

    @api.multi
    def _set_simple_price(self):
        self.ensure_one()
        if len(self.pricelist_ids) == 1:
            self.pricelist_ids[0].price = self.simple_price

    @api.multi
    def _set_simple_discount(self):
        self.ensure_one()
        if len(self.pricelist_ids) == 1:
            self.pricelist_ids[0].discount = self.simple_discount

    @api.multi
    def _set_simple_discount2(self):
        self.ensure_one()
        if len(self.pricelist_ids) == 1:
            self.pricelist_ids[0].discount2 = self.simple_discount2

    @api.multi
    def _set_simple_discount3(self):
        self.ensure_one()
        if len(self.pricelist_ids) == 1:
            self.pricelist_ids[0].discount3 = self.simple_discount3

    # View Section
    @api.multi
    def create_simple_line(self):
        self.ensure_one()
        partnerinfo_obj = self.env['pricelist.partnerinfo']
        vals = {'min_quantity': 0, 'price': 0}
        defaults = partnerinfo_obj._add_missing_default_values({})
        vals.update(defaults)
        if len(self.pricelist_ids) == 0:
            vals['suppinfo_id'] = self.id
            partnerinfo_obj.create(vals)
        else:
            # This case occures in the case of concurrent access
            lines = ';\n - '.join([_(
                'qty : %s - price : %s') % (x.min_quantity, x.price)
                for x in self.pricelist_ids])
            raise UserError(_(
                "You can not create a simple supplier line for '%s'"
                " product because it has already one (or many)"
                " lines.\n\n - %s" % (self.product_tmpl_id.name, lines)))
        return True

    @api.multi
    def edit_multiple_lines(self):
        self.ensure_one()
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.supplierinfo',
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'target': 'new',
            'nodestroy': True,
        }
