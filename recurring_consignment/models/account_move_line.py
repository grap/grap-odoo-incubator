# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Columns Section
    consignment_invoice_id = fields.Many2one(
        string='Consignment Commission Invoice',
        comodel_name='account.invoice')

    consignment_commission = fields.Float(
        string='Consignment Commission Rate')
