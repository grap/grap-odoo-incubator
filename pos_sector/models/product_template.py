# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Columns section
    sector_id = fields.Many2one(
        comodel_name='pos.sector', string='Point of Sale Sector')
