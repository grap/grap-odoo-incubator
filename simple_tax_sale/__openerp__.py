# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale - Simple Tax',
    'summary': 'Easy Switch between VAT Excluded and VAT Included For Sale',
    'version': '8.0.1.0.0',
    'category': 'Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'simple_tax_account',
        'sale',
    ],
    'data': [
        'views/view_sale_order.xml',
    ],
    'demo': [
        'demo/sale_order.xml',
    ],
    'auto_install': True,
    'installable': False,
}
