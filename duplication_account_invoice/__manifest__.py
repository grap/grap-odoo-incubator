# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Invoice - Duplication',
    'summary': 'Duplication Tools for Invoices with a given frequency',
    'version': '12.0.1.0.1',
    'category': 'Account',
    'author': 'GRAP, Odoo Community Association (OCA)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'views/view_account_invoice_duplication_wizard.xml',
        'views/action.xml',
    ],
    'installable': True,
}
