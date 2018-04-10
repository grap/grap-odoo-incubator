# -*- coding: utf-8 -*-
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'POS Load Done Orders',
    'summary': 'Point Of Sale - Load Done Orders',
    'version': '8.0.1.1.0',
    'author': 'GRAP,Odoo Community Association (OCA)',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'website': 'https://odoo-community.org/',
    'data': [
#        'views/view_pos_config.xml',
        'views/pos_done_order_load.xml',
    ],
    'demo': [
    ],
    'qweb': [
        'static/src/xml/pos_done_order_load.xml',
    ],
}
