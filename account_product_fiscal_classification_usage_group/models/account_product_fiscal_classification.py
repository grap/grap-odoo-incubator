# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields


class AccountProductFiscalClassification(models.Model):
    _inherit = 'account.product.fiscal.classification'

    usage_group_id = fields.Many2one(
        comodel_name='res.groups', string="Usage Group", help="If defined"
        ", the user should be member to this group, to use this fiscal"
        " classification when creating or updating products")
