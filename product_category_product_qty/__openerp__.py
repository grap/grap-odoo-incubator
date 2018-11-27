# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product Category - Product Quantity',
    'version': '8.0.1.0.0',
    'category': 'Product',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
    ],
    'data': [
        'views/view_product_category.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
    'images': [
        'static/description/product_category_tree.png',
        'static/description/product_category_form.png',
    ],
    'installable': True,
}
