# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Point Of Sale - Multiple Cash Control Automatic solve',
    'summary': "Allow user to solve very quickly each statement with one item",
    'version': '8.0.3.0.0',
    'category': 'Point of Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'pos_multiple_control',
    ],
    'data': [
        'views/view_pos_session.xml',
        'views/view_pos_config.xml',
    ]
}
