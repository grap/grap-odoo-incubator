# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Sale Order - Duplication',
    'summary': 'Duplication Tools for Sale Orders with a given frequency',
    'version': '8.0.1.0.0',
    'category': 'Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'sale_order_dates',
    ],
    'data': [
        'views/view_sale_order_duplication_wizard.xml',
        'views/action.xml',
    ],
    'installable': True,
}
