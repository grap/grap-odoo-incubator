# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models

import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Colum section
    standard_price_vat_incl = fields.Float(
        string='Cost VAT Included', compute='_compute_standard_price_vat_incl',
        digits_compute=dp.get_precision('Product Price'), store=True,
        help="Cost price of the product based on:\n"
        "* Cost;\n"
        "* Customer Taxes;\n"
        "This cost will be Cost per Taxes and works only if you have"
        " set Taxes with VAT include in the price")

    # Compute Section
    @api.depends('standard_price', 'taxes_id')
    def _compute_standard_price_vat_incl(self):
        for template in self:
            tax_data = template.taxes_id.compute_all(
                template.standard_price, 1, force_excluded=True)
            template.standard_price_vat_incl = tax_data['total_included']
