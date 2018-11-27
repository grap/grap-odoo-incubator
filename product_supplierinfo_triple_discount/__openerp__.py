# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Triple Discounts in product supplier info",
    "version": "8.0.1.0.0",
    "author": "GRAP",
    "category": "Purchase Management",
    "website": "https://odoo-community.org",
    "license": "AGPL-3",
    "depends": [
        'product_supplierinfo_discount',
        'purchase_triple_discount',
    ],
    "data": [
        'views/view_product_supplierinfo.xml',
    ],
    "demo": [
        'demo/res_groups.xml',
        'demo/product_template.xml',
    ],
    'images': [
        'static/description/product_supplierinfo_form.png',
    ],
    "installable": True,
}
