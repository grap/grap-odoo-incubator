# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields

SIMPLE_TAX_TYPE_KEYS = [
    ('none', 'Undefined'),
    ('excluded', 'Exclude Tax in Prices'),
    ('included', 'Include Tax in Prices'),
]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    simple_tax_type = fields.Selection(
        selection=SIMPLE_TAX_TYPE_KEYS, string='Tax Type', required=True,
        default='none')
