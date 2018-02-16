# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def get_income_expense_accounts(self):
        """ get the income and expense accounts related to product.
        @return: dictionary which contains information regarding
            income and expense accounts
        """
        self.ensure_one()
        categ = self.categ_id
        income_account = (
            self.property_account_income or (
                categ and categ.property_account_income_categ or False))

        expense_account = (
            self.property_account_expense or (
                categ and categ.property_account_expense_categ or False))

        return {
            'account_income': income_account,
            'account_expense': expense_account,
        }
