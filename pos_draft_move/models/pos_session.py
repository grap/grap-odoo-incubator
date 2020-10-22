# coding: utf-8
# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    generate_draft_moves = fields.Boolean(
        string="Generate Draft Moves", default=False)

    @api.multi
    def wkf_action_close(self):
        super(PosSession, self.with_context(
            pos_draft_move=True)).wkf_action_close()
