# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    iface_load_done_order = fields.Boolean(
        string='Load Done Orders', default=True)

    iface_load_done_order_max_qty = fields.Integer(
        string='Max Done Orders Quantity To Load', default=10, required=True)
