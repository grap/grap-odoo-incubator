# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Fiscal Position - Tax Excluded to Included',
    'summary': 'Allow to map from tax excluded to tax included',
    'version': '8.0.1.0.0',
    'category': 'Accounting',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/view_account_fiscal_position.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/account_tax.xml',
        'demo/account_fiscal_position.xml',
        'demo/product_product.xml',

    ],
    'installable': False,
}
