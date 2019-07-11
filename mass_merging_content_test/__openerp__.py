# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Mass Merging Content (Test Module)',
    'version': "8.0.1.0.0",
    'author': 'GRAP',
    'summary': "Test the module mass_merging_content",
    'category': 'Tools',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'mass_merging_content',
        'account',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/mass_merging_content.xml',
        'demo/mass_merging_content_line.xml',
        'demo/account_invoice.xml',
        'demo/account_invoice_line.xml',
    ],
    'installable': False,
}
