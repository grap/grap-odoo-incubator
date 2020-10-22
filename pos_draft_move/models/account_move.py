# coding: utf-8
# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from openerp import api, models


_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def post(self):
        if self.env.context.get("pos_draft_move", False):
            _logger.warning(
                "The close of the session %s will not post entries" % (
                    ",".join(self.mapped("name")))
            )
            return
        super(AccountMove, self).post()
