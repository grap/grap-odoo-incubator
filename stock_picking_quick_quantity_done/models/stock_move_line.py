# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_initial_demand = fields.Float(
        string='Initial Demand',
        default=0.0, required=True, states={'done': [('readonly', True)]},
        related='move_id.product_uom_qty')
