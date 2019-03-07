# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Columns Section
    autosolve_product = fields.Many2one(
        string='Product used to autosolve control difference in pos session',
        comodel_name='product.template',
        domain="['|', ('income_pdt', '=', True), ('expense_pdt', '=', True)]",
        default="")

    autosolve_limit = fields.Float(
        string='Limit for autosolving bank statement',
        default=20)
