# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Point of Sale - Street Market',
    'version': '8.0.2.0.0',
    'category': 'Point of Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/view_market_place.xml',
        'views/view_pos_order.xml',
        'views/view_pos_config.xml',
        'views/action.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/pos_street_market.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/market_place.xml',
    ],
}
