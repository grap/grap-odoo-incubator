# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields
import openerp.addons.decimal_precision as dp


class WizardUpdateInvoiceSupplierinfoLine(models.TransientModel):
    _inherit = 'wizard.update.invoice.supplierinfo.line'

    current_discount2 = fields.Float(
        string='Current Discount %2', readonly=True,
        digits_compute=dp.get_precision('Discount'))

    new_discount2 = fields.Float(
        string='New Discount %2', required=True,
        digits=dp.get_precision('Product Price'))

    current_discount3 = fields.Float(
        string='Current Discount %3', readonly=True,
        digits_compute=dp.get_precision('Discount'))

    new_discount3 = fields.Float(
        string='New Discount %3', required=True,
        digits=dp.get_precision('Product Price'))

    @api.multi
    def _prepare_partnerinfo(self, supplierinfo):
        res = super(WizardUpdateInvoiceSupplierinfoLine, self).\
            _prepare_partnerinfo(supplierinfo)
        res['discount2'] = self.new_discount2
        res['discount3'] = self.new_discount3
        return res
