# coding: utf-8
# Copyright (C) 2019-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.model
    def _fix_tax_included_price(self, price, prod_taxes, line_taxes):
        """Subtract tax amount from price when corresponding "price included"
        taxes do not apply. (for tax excluded)"""
        print "_fix_tax_included_price::OVERLOAD"
        res = super(AccountTax, self)._fix_tax_included_price(
            price, prod_taxes, line_taxes)
        if price != res:
            return res
        excl_tax = [
            tax for tax in prod_taxes
            if tax.id not in line_taxes and not tax.price_include]
        if excl_tax:
            print ">>>> FIX INCLUDED"
            return prod_taxes.compute_all(price, 1)['total_included']
        print ">>>> DONT FIX"
        return price
