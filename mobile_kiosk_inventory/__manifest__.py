# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mobile Kiosk Inventory",
    "version": "12.0.1.1.3",
    "author": "GRAP",
    "summary": "Mobile interface to make inventories",
    "category": "Tools",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "maintainers": ["legalsylvain"],
    "depends": [
        "stock",
        "mobile_kiosk_abstract",
    ],
    "data": [
        "views/templates.xml",
        "views/view_stock_inventory.xml",
        "data/mobile_kiosk_application.xml",
    ],
    "qweb": [
        "static/src/xml/mobile_kiosk_inventory.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
    ],
    "installable": True,
}
