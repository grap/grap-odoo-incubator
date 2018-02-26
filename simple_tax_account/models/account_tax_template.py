# coding: utf-8
# Copyright (C) 2018-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, exceptions, models


class AccountTaxTemplate(models.Model):
    _inherit = 'account.tax.template'

    # Columns Section
    simple_template_id = fields.Many2one(
        comodel_name='account.tax.template', string='Related Tax Template',
        help="If the current tax template is flagged as included,"
        " set here a tax template flagged as excluded. Otherwise,"
        " set a tax flagged as included.")

    # Constraints Section
    @api.multi
    @api.constrains('price_include', 'simple_template_id')
    def _check_simple_tax(self):
        for template in self:
            if template.simple_template_id:
                if (template.price_include ==
                        template.simple_template_id.price_include):
                    raise exceptions.ValidationError(_(
                        "The current Tax Template and the Related Tax"
                        " Teamplate have the same settings for the field"
                        " 'Tax Included in Price'"))
