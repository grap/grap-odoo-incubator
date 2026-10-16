# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mobile Kiosk Inventory",
    "version": "16.0.1.0.0",
    "author": "GRAP",
    "summary": "Mobile interface to make inventories",
    "category": "Tools",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "maintainers": ["legalsylvain"],
    "depends": [
        "mobile_kiosk_abstract",
        "stock_inventory_mgmt",
    ],
    "data": [
        "views/view_stock_inventory.xml",
        "views/view_product_product.xml",
        "security/ir.model.access.csv",
        "data/mobile_kiosk_application.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mobile_kiosk_inventory/static/src/InventoryAction/**/*",
            "mobile_kiosk_inventory/static/src/SetInventory/**/*",
            "mobile_kiosk_inventory/static/src/SetProduct/**/*",
            "mobile_kiosk_inventory/static/src/SetQuantity/**/*",
        ],
    },
    "installable": True,
}
