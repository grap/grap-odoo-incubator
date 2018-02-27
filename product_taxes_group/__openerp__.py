# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product - Taxes Group',
    'summary': 'Simplify taxes management for products with Taxes Group',
    'version': '0.1',
    'category': 'product',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'stock',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/ir_model_access.yml',
        'view/action.xml',
        'view/view.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/account_tax.yml',
        'demo/tax_group.yml',
        'demo/product_product.yml',
    ],
    'installable': True,
}
