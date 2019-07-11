# -*- coding: utf-8 -*-
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'POS Load Done Orders',
    'summary': 'Point Of Sale - Load Done Orders',
    'version': '8.0.1.2.0',
    'author': 'GRAP',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'website': 'https://odoo-community.org/',
    'data': [
        'views/view_pos_config.xml',
        'views/pos_done_order_load.xml',
    ],

    'qweb': [
        'static/src/xml/pos_done_order_load.xml',
    ],
    'images': [
        'static/description/pos_config_form.png',
        'static/description/pos_done_order_list.png',
        'static/description/pos_load_done_order_button.png',
    ],
    'installable': False,
}
