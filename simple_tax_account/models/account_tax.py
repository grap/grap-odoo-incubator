# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class AccountTax(models.Model):
    _inherit = 'account.tax'

    # Columns Section
    simple_tax_id = fields.Many2one(
        comodel_name='account.tax', string='Related Tax',
        domain="[('id', '!=', id),"
        "('amount', '=', amount),"
        "('type', '=', 'percent'),"
        "('price_include', '!=', price_include)]",
        help="If the current tax is flagged as included, set here a tax"
        " flagged as excluded. Otherwise, set a tax flagged as included.")

    # Constraints Section
    @api.multi
    @api.constrains('amount', 'type', 'price_include', 'simple_tax_id')
    def _check_simple_tax(self):
        for tax in self.filtered(lambda x: x.simple_tax_id):
            if tax.price_include == tax.simple_tax_id.price_include:
                raise ValidationError(_(
                    "The current Tax and the Related Tax have the same"
                    " settings for the field 'Tax Included in Price'"))
            if tax.amount != tax.simple_tax_id.amount:
                raise ValidationError(_(
                    "The current Tax and the Related Tax don't have the"
                    " same amount"))
            if tax.type != 'percent':
                raise ValidationError(_(
                    "Simple Tax Acount module is not designed for"
                    " taxes if type is not 'percentage'"))

    # Overload Section
    @api.model
    def create(self, vals):
        res = super(AccountTax, self).create(vals)
        res._propagate_simple_tax(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super(AccountTax, self).write(vals)
        self._propagate_simple_tax(vals)
        return res

    # Custom Section
    @api.multi
    def _propagate_simple_tax(self, vals):
        if 'simple_tax_id' in vals.keys() and\
                not self.env.context.get('dont_propagate_simple_tax', False):
            for tax in self.with_context(dont_propagate_simple_tax=True):
                if tax.simple_tax_id:
                    # tax has been changed or set
                    tax.simple_tax_id.simple_tax_id = tax.id
                # Remove previous links
                obsolete_taxes = self.search([
                    ('id', '!=', tax.simple_tax_id.id),
                    ('simple_tax_id', '=', tax.id),
                ])
                obsolete_taxes.with_context(
                    dont_propagate_simple_tax=True).write({
                        'simple_tax_id': False})

    def _translate_simple_tax(self, partner, price_unit, taxes):
        """Return an dict with price_unit and tax_ids keys depending of
        a partner setting."""
        res = {
            'price_unit': price_unit,
            'tax_ids': taxes.ids,
        }

        if not partner or len(taxes) == 0 or not price_unit:
            # Nothing to do
            return res

        if partner.simple_tax_type == 'none':
            # Tax Changes is not required
            return res

        is_percent = all([tax.type == 'percent' for tax in taxes])
        is_same_type = all([
            tax.price_include == taxes[0].price_include for tax in taxes])

        if not (is_percent and is_same_type):
            # Tax changes is not possible
            # Note: This algorithm could be improved to manage this case.
            return res

        if ((not taxes[0].price_include and
                partner.simple_tax_type == 'excluded') or
            (taxes[0].price_include and
                partner.simple_tax_type == 'included')):
            # Tax changes is not required
            return res

        new_taxes = []
        for tax in taxes:
            if not tax.simple_tax_id:
                raise ValidationError(_(
                    "Please ask to your accountant to set a Related"
                    " Tax for the tax %s.") % (tax.name))
            if tax.price_include:
                price_unit = price_unit / (1 + tax.amount)
            else:
                price_unit = price_unit * (1 + tax.amount)
            new_taxes.append(tax.simple_tax_id)
        return {
            'price_unit': price_unit,
            'tax_ids': [tax.id for tax in new_taxes],
        }
