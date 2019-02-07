# coding: utf-8
# Copyright (C) 2018-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class AccountTaxTemplate(models.Model):
    _inherit = 'account.tax.template'

    # Columns Section
    simple_template_id = fields.Many2one(
        comodel_name='account.tax.template', string='Related Tax Template',
        domain="[('id', '!=', id),"
        "('amount', '=', amount),"
        "('type', '=', 'percent'),"
        "('price_include', '!=', price_include)]",
        help="If the current tax template is flagged as included,"
        " set here a tax template flagged as excluded. Otherwise,"
        " set a tax flagged as included.")

    # Constraints Section
    @api.multi
    @api.constrains('amount', 'type', 'price_include', 'simple_template_id')
    def _check_simple_tax_template(self):
        for tmpl in self.filtered(lambda x: x.simple_template_id):
            if tmpl.price_include == tmpl.simple_template_id.price_include:
                raise ValidationError(_(
                    "The current Template and the Related Template have the"
                    " same settings for the field 'Tax Included in Price'"))
            if tmpl.amount != tmpl.simple_template_id.amount:
                raise ValidationError(_(
                    "The current Template and the Related Template don't have"
                    " the same amount"))
            if tmpl.type != 'percent':
                raise ValidationError(_(
                    "Simple Tax Acount module is not designed for"
                    " tax templates if type is not 'percentage'"))

    # Overload Section
    @api.model
    def create(self, vals):
        res = super(AccountTaxTemplate, self).create(vals)
        res._propagate_simple_tax_template(vals)
        return res

    @api.multi
    def write(self, vals):
        res = super(AccountTaxTemplate, self).write(vals)
        self._propagate_simple_tax_template(vals)
        return res

    # Custom Section
    @api.multi
    def _propagate_simple_tax_template(self, vals):
        if 'simple_template_id' in vals.keys() and\
                not self.env.context.get('dont_propagate_simple_tax', False):
            for tmpl in self.with_context(dont_propagate_simple_tax=True):
                if tmpl.simple_template_id:
                    # related template has been changed or set
                    tmpl.simple_template_id.simple_template_id = tmpl.id
                # Remove previous links
                obsolete_taxes = self.search([
                    ('id', '!=', tmpl.simple_template_id.id),
                    ('simple_template_id', '=', tmpl.id),
                ])
                obsolete_taxes.with_context(
                    dont_propagate_simple_tax=True).write({
                        'simple_template_id': False})
