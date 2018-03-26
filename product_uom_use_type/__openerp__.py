# coding: utf-8
# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product UoM - Use Type",
    "summary": "Define UoM for Sale and / or for Purchase purpose",
    "version": "8.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "GRAP, Odoo Community Association (OCA)",
    "license": "AGPL-3",

    "depends": [
        "product",
    ],
    "data": [
        'views/view_product_uom.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/product_uom.xml',
    ],
    "installable": True,
}
