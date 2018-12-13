# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Mass Operation Abstract',
    'version': "8.0.1.0.0",
    'author': 'GRAP,Odoo Community Association (OCA)',
    'summary': "Abstract Tools used for modules that realize operation on"
    "many items",
    'category': 'Tools',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'views/menu.xml',
        'views/view_mass_operation_mixin.xml',
        'views/view_mass_operation_wizard_mixin.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
}
