# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        related='config_id.company_id', store=True, readonly=True)
