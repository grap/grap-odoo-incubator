# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base - Company Legal Information',
    'version': '8.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Adds Legal informations on company model',
    'author': 'Akretion,GRAP',
    'website': 'http://www.akretion.com',
    'depends': [
        'report',
    ],
    'data': [
        'views/view_res_company.xml',
        'views/external_layout_footer.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/res_company.xml',
    ],
    'installable': False,
}
