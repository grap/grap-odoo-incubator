# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Columns section
    barcode_warning_regexpr = fields.Char(
        string='Regular Expression for Barcode Warning',
        default=lambda s: s._default_barcode_warning_regexpr())

    @api.multi
    def _default_barcode_warning_regexpr(self):
        return '[0-9]{8,13}'
