# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Columns section
    payment_limit = fields.Float(string='Payment Limit', default=1000)
