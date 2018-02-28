# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    mail_send_bcc = fields.Boolean(
        string='Send Email Bcc', default=True,
        help="If checked, you will receive each mail in bcc mode"
        " for each mail you will send using OpenERP.")
