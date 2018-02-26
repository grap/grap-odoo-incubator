# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class TaxGroup(models.Model):
    _inherit = 'tax.group'

    # Columns Section
    consignor_partner_id = fields.Many2one(
        string='Consignor', comodel_name='res.partner',
        domain="[('is_consignor', '=', True)]")

    # Constrains Section
    @api.constrains('supplier_tax_ids', 'consignor_partner_id')
    def _check_consignor_supplier_tax_ids(self):
        for tax_group in self:
            if (tax_group.consignor_partner_id and
                    len(tax_group.supplier_tax_ids)):
                raise UserError(_(
                    "You can not set Supplier Taxes for taxes Groups used for"
                    " consignment"))
