# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product - Supplier Info Quick Edit',
    'summary': 'Provides Wizard to manage easily Supplierinfo',
    'version': '8.0.4.0.0',
    'category': 'Purchase',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
        'product_supplierinfo_discount',
        'product_supplierinfo_triple_discount',
    ],
    'data': [
        'view/view_product_supplierinfo_create_purchase_order.xml',
        'view/view_product_supplierinfo.xml',
        'view/action.xml',
        'view/view_res_partner.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
    'images': [
        'static/description/supplierinfo_tree.png',
    ],
    'installable': True,
}
