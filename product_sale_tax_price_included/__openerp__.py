# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product Sale Tax Price Included',
    'summary': "Provides new fields Sale Prices w/o taxes",
    'version': '8.0.1.0.0',
    'category': 'Sale',
    'website': 'http://www.grap.coop',
    'author': 'GRAP',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/view_product_template.xml',
    ],
    'demo': [
        'demo/account_tax.xml',
        'demo/product_template.xml'
    ],
    'images': [
        'static/description/product_different_prices.png',
        'static/description/product_tax_excluded.png',
        'static/description/product_tax_included.png',
        'static/description/product_tax_included_and_not.png',
        'static/description/taxes_creation.png',
    ],
    'installable': True,
}
