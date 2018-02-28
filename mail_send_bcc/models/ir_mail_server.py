# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models
from email.Utils import COMMASPACE


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    # Overload Section
    @api.model
    def send_email(
            self, message, mail_server_id=None, smtp_server=None,
            smtp_port=None, smtp_user=None, smtp_password=None,
            smtp_encryption=None, smtp_debug=False):
        if self.env.user.mail_send_bcc:
            if message['Bcc']:
                message['Bcc'] = message['Bcc'].join(
                    COMMASPACE, message['From'])
            else:
                message['Bcc'] = message['From']
        return super(IrMailServer, self).send_email(
            message, mail_server_id=mail_server_id, smtp_server=smtp_server,
            smtp_port=smtp_port, smtp_user=smtp_user,
            smtp_password=smtp_password, smtp_encryption=smtp_encryption,
            smtp_debug=smtp_debug)
