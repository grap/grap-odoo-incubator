# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, models
from openerp.exceptions import Warning as UserError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # Columns section
    @api.multi
    def copy(self, default=None):
        self.ensure_one()

        default = default or {}
        session_id = self._default_session()
        if session_id:
            default['session_id'] = session_id
        else:
            raise UserError(_(
                "Unable to copy the order because there is no opened session"
                " associated to the current user %s.\n"
                " Please open a session and try again.") % (
                    self.env.user.name))
        return super(PosOrder, self).copy(default=default)
