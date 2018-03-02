# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class PosSessionOpening(models.TransientModel):
    _inherit = 'pos.session.opening'

    @api.multi
    def open_session_cb(self):
        self.ensure_one()
        # Check if some opening / opened session exists
        session_obj = self.env['pos.session']
        sessions = session_obj.search([
            ('user_id', '=', self.env.uid),
            ('config_id', '=', self.pos_config_id.id),
            ('state', 'in', ['opened', 'opening_control']),
        ], limit=1)
        if sessions:
            # An opening / opened session exists
            session = sessions[0]
        else:
            # Create a session
            session = session_obj.create({
                'user_id': self.env.uid,
                'config_id': self.pos_config_id.id,
            })

        if session.state == 'opening_control':
            return self._open_session(session.id)
        return self.open_ui()
