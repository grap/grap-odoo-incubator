# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Account Product - Fiscal Classification - Restricted Access',
    'summary': 'Restricted Access for Product Fiscal Classification',
    'version': '8.0.1.0.0',
    'category': 'Accounting',
    'author': 'GRAP',
    'license': 'AGPL-3',
    'depends': [
        'account_product_fiscal_classification',
    ],
    'data': [
        'views/view_account_product_fiscal_classification.xml',
    ],
    'images': [
        'static/description/product_template_warning.png',
        'static/description/account_product_fiscal_classification_form.png',
    ],
    'installable': False,
}
