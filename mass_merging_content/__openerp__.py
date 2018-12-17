# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Mass Merging Content',
    'version': "8.0.1.0.0",
    'author': 'GRAP',
    'summary': "Merge lines according given settings, for any models",
    'category': 'Tools',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'mass_operation_abstract',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/view_mass_merging_content.xml',
        'views/view_mass_merging_content_wizard.xml',
    ],
    'images': [
        'static/description/account_invoice_form_after.png',
        'static/description/account_invoice_form_before.png',
        'static/description/account_invoice_tree.png',
        'static/description/mass_merging_content_form.png',
        'static/description/wizard_form_ok.png',
        'static/description/wizard_form_warning.png',
    ],
}
