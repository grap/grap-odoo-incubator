# -*- coding: utf-8 -*-
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class PosCategory(models.Model):
    _inherit = 'pos.category'

    # Column Section
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=lambda self: self.env.user.company_id)
