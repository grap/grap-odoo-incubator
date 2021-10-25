# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (https://twitter.com/pondupont)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Category - Product Quantity",
    "version": "12.0.1.1.0",
    "category": "Product",
    "author": "GRAP, " "Odoo Community Association (OCA)",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "views/view_product_category.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
    ],
    "images": [
        "static/description/product_category_tree.png",
        "static/description/product_category_form.png",
    ],
    "installable": True,
}
