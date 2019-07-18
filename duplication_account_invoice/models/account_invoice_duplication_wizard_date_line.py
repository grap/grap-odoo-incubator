# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountInvoiceDuplicationWizardDateLine(models.TransientModel):
    _name = 'account.invoice.duplication.wizard.date.line'

    wizard_id = fields.Many2one(
        comodel_name='account.invoice.duplication.wizard')

    date_invoice = fields.Date(
        string='Invoice Date', required=True)

    date_due = fields.Date(
        string='Due Date', required=True)
