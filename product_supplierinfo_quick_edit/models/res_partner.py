# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    supplierinfo_qty = fields.Integer(
        string='Product Infos Quantity', compute='_compute_supplierinfo_qty')

    @api.multi
    def _compute_supplierinfo_qty(self):
        supplierinfo_obj = self.env['product.supplierinfo']
        for partner in self:
            partner.supplierinfo_qty = supplierinfo_obj.search_count(
                [('name', '=', partner.id)])
