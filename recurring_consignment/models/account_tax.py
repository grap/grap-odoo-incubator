# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class AccountTax(models.Model):
    _inherit = 'account.tax'

    # Columns Section
    consignor_partner_id = fields.Many2one(
        string='Consignor', comodel_name='res.partner',
        domain="[('is_consignor', '=', True)]")

    # Onchange Section
    @api.onchange('consignor_partner_id')
    def on_change_consignor_partner_id(self):
        if not self.consignor_partner_id:
            return
        partner = self.consignor_partner_id
        self.account_collected_id = partner.consignment_account_id.id
        self.account_paid_id = partner.consignment_account_id.id

    # Constrains Section
    @api.constrains(
        'consignor_partner_id', 'account_collected_id', 'account_paid_id')
    def _check_consignor_taxes(self):
        for tax in self:
            if tax.consignor_partner_id and (
                    tax.consignor_partner_id.consignment_account_id.id !=
                    tax.account_collected_id.id or
                    tax.consignor_partner_id.consignment_account_id.id !=
                    tax.account_paid_id.id):
                raise UserError(_(
                    "You have to set the same accounts as the supplier account"
                    " of the selected consignor."))
