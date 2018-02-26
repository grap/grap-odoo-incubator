# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class AccountTaxCode(models.Model):
    _inherit = 'account.tax.code'

    # Columns Section
    consignment_product_id = fields.Many2one(
        string='Consignment Product', comodel_name='product.product',
        domain="[('is_consignment_commission', '=', True)]",
        help="Set a 'Sales commission' product for consignment sales.\n"
        "If not set, transaction will not be commissioned. (this case is"
        " usefull to avoid to commission taxes transaction, because in"
        " most cases, commissions are computed on without taxes amount).")
