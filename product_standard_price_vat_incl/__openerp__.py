# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product - Standard Price VAT Included',
    'version': '8.0.1.0.0',
    'category': 'Product',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'data/product_price_type.xml',
        'views/view_product_template.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/product_pricelist.xml',
        'demo/account_tax.xml',
        'demo/product_template.xml',
    ],
    'installable': True,
}
