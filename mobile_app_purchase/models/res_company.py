# coding: utf-8
# Copyright (C) 2016 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    mobile_purchase_product_field_ids = fields.Many2many(
        comodel_name='ir.model.fields', string='Product Fields',
        domain=[('model', 'in', ['product.product'])])

    mobile_purchase_supplierinfo_field_ids = fields.Many2many(
        comodel_name='ir.model.fields', string='Supplier Info Fields',
        domain=[('model', 'in', ['product.supplierinfo'])])
