# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock - Merge Inventories",
    "summary": "Allow to merge multiples partial inventories",
    "version": "12.0.1.1.2",
    "category": "Stock",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "views/view_stock_inventory_line.xml",
        "views/view_stock_inventory.xml",
        "views/view_wizard_stock_inventory_merge.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_product.xml",
        "demo/stock_inventory.xml",
    ],
    "images": [
        "static/description/stock_inventory_disabled_warning.png",
        "static/description/stock_inventory_form_complete_zero.png",
        "static/description/stock_inventory_form_duplicate.png",
        "static/description/stock_inventory_tree_merge.png",
    ],
    "installable": True,
}
