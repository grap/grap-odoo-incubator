# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Columns Section
    is_consignor = fields.Boolean(string='Is Consignor')

    consignment_commission = fields.Float(string='Consignment Commission Rate')

    consignment_account_id = fields.Many2one(
        string='Consignment Account', comodel_name='account.account',
        domain="[('type', 'in', ['other', 'receivable', 'payable'])]")

    consignor_tax_group_ids = fields.One2many(
        string='Taxes Groups', comodel_name='tax.group',
        inverse_name='consignor_partner_id', readonly=True)

    # Constrains Section
    @api.constrains(
        'is_consignor', 'consignment_commission', 'consignment_account_id')
    def _check_is_consignor_consignment_account_id(self):
        for partner in self:
            if partner.is_consignor:
                if not partner.consignment_account_id:
                    raise UserError(_(
                        "A Consignor must have a 'Consignment Account'"
                        " defined."))
            else:
                if (partner.consignment_account_id or
                        partner.consignment_commission != 0):
                    raise UserError(_(
                        "A Non Consignor partner can not have 'Consignment"
                        " Commission' neither 'Consignment Account' defined."))

    # Overload Section
    @api.model
    def create(self, vals):
        vals = self._prepare_vals_consignor(vals)
        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        self._prevent_uncheck_is_consignor(vals)
        vals = self._prevent_change_is_consignor(vals)
        return super(ResPartner, self).write(vals)

    # Custom Section
    @api.model
    def _prepare_vals_consignor(self, vals):
        if vals.get('is_consignor', False):
            vals.update({
                'simple_tax_type': 'excluded',
                'property_account_payable': vals.get(
                    'consignment_account_id', False),
                'property_account_receivable': vals.get(
                    'consignment_account_id', False),
            })
        return vals

    @api.multi
    def _prevent_uncheck_is_consignor(self, vals):
        """ prevent possibility to uncheck is_consignor for partners"""
        if not vals.get('is_consignor', True) and\
                any(self.mapped('is_consignor')):
            raise UserError(_(
                "You can not unset consignor setting on partner.\n"
                " Please create a new one if you want to do so."))

    @api.multi
    def _prevent_change_is_consignor(self, vals):
        """ prevent to write incorrect values for consignors"""
        if any(self.mapped('is_consignor')):
            if len(self) == 1:
                vals.pop('simple_tax_type', False)
                vals.pop('property_account_payable', False)
                vals.pop('property_account_receivable', False)
                if 'consignment_account_id' in vals:
                    vals.update({
                        'property_account_payable': vals.get(
                            'consignment_account_id', False),
                        'property_account_receivable': vals.get(
                            'consignment_account_id', False),
                    })
            elif set([
                    'simple_tax_type', 'property_account_payable',
                    'property_account_receivable',
                    'consignment_account_id']) & set(vals.keys()):
                raise UserError(_(
                    "You can not change this settings (Tax Type and"
                    " Accounting Properties) for many partners if some"
                    " of them are consignors."))
        return vals
