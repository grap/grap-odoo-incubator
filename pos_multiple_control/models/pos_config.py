# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    # Columns Section
    autosolve_pos_move_reason = fields.Many2one(
        string="Autosolve pos move reason",
        description="Product used to autosolve control difference in pos session",
        comodel_name="pos.move.reason",
        domain="['|', ('is_income_reason', '=', True), ('is_expense_reason', '=', True)]",
        default="",
    )

    autosolve_limit = fields.Float(
        string="Autosolve limit",
        description="Limit for autosolving bank statement", default=20
    )
