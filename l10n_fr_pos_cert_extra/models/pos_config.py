# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.tools.config import config


class PosConfig(models.Model):
    _inherit = 'pos.config'

    _SELECTION_HASH_PRINT_LEGACY = [
        ('no', 'Do not Print Hash'),
        ('warning', 'Print Hash or Mark a Warning'),
        ('block', 'Print Hash or Prevent Printing'),
    ]

    l10n_fr_prevent_print = fields.Char(
        string='Prevent Uncertified Bill (Computed)',
        compute='_compute_l10n_fr_prevent_print',
        help="Indicate what is the behaviour of the Point of Sale, if"
        " the server is unreachable\n"
        "This field is a computed field, based on 'Prevent Uncertified Bill'"
        " and the value of the key 'l10n_fr_certification_mode' in the server"
        " configuration file.")

    l10n_fr_prevent_print_legacy = fields.Selection(
        string='Prevent Uncertified Bill', required=True, default='no',
        selection=_SELECTION_HASH_PRINT_LEGACY, help="Indicate what is the"
        " behaviour of the Point of Sale\n"
        " * 'Do not Print Hash': Normal behaviour\n"
        " * 'Print Hash or Mark a Warning': A warning text will be printed"
        " on the bill if the server is unreachable\n"
        " * 'Print Hash or Prevent Printing': The downgraded mode is disabled"
        " and the cashier will not have the possibility to give the bill to"
        " the customer, if there is a network problem. This is the most secure"
        " mode from a point of view of certification but you have to ensure"
        " that network connection is reliable.\n\n"
        " Note : This setting has no effect, if server configuration file"
        " has a value different to 'legacy', for the key"
        " 'l10n_fr_certification_mode'")

    # Compute Section
    @api.multi
    def _compute_l10n_fr_prevent_print(self):
        file_value = config.get('l10n_fr_certification_mode', 'legacy')
        for pos_config in self:
            if file_value == 'legacy':
                pos_config.l10n_fr_prevent_print =\
                    pos_config.l10n_fr_prevent_print_legacy
            else:
                pos_config.l10n_fr_prevent_print = file_value
