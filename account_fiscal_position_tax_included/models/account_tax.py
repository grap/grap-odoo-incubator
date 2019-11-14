# coding: utf-8
# Copyright (C) 2019-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _fix_tax_included_price(self, price, prod_taxes, line_taxes):
        """Subtract tax amount from price when corresponding "price included"
        taxes do not apply. (for tax excluded)"""
        res = super(AccountTax, self)._fix_tax_included_price(
            price, prod_taxes, line_taxes
        )

        if price != res:
            return res
        dest_taxes = self.browse(line_taxes)
        if any([x.price_include for x in dest_taxes]) and not any(
            [x.price_include for x in prod_taxes]
        ):
            # it's a switch between vat exc and vat incl
            return price * (1 + dest_taxes[0].amount)
        return res
