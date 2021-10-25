# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Inventory - Valuation",
    "version": "12.0.1.1.2",
    "category": "Stock",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["stock"],
    "data": [
        "views/view_stock_inventory.xml",
        "views/view_stock_inventory_line.xml",
    ],
    "demo": [
        "demo/product_product.xml",
        "demo/stock_inventory.xml",
    ],
    "installable": True,
}
