# coding: utf-8
# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase - Simple Tax',
    'summary': 'Switch between VAT Excluded and VAT Included For Purchase',
    'version': '8.0.1.0.0',
    'category': 'Purchase',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'simple_tax_account',
        'purchase',
    ],
    'data': [
        'views/view_purchase_order.xml',
    ],
    'demo': [
        'demo/purchase_order.xml',
    ],
    'images': [
        'static/description/purchase_mixed_taxes.png',
        'static/description/purchase_harmonized_taxes.png',
    ],
    'auto_install': True,
    'installable': False,
}
