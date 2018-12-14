# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Mass Linking',
    'version': "8.0.1.0.0",
    'author': 'GRAP',
    'summary': "Provide the possibility to see any related items of selected"
    "items",
    'category': 'Tools',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'mass_operation_abstract',
    ],
    'data': [
        'views/view_mass_linking.xml',
        'views/view_mass_linking_wizard.xml',
    ],
    'demo': [
        'demo/mass_linking.xml',
    ],
}
