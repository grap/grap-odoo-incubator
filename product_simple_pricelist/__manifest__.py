# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product - Simple Pricelist",
    "summary": "Provides Wizard to manage easily Pricelist By Products",
    "version": "12.0.1.1.5",
    "category": "Product",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "product",
        "sale",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/view_product_product.xml",
        "views/view_product_pricelist.xml",
        "views/menu.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_pricelist.xml",
    ],
    "images": [
        "static/description/pricelist_item_form.png",
        "static/description/product_pricelist_tree.png",
        "static/description/simple_price_list_item.png",
        "static/description/wizard_form.png",
    ],
    "installable": True,
}
