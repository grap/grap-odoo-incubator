# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mobile Kiosk Purchase",
    "version": "12.0.1.1.5",
    "author": "GRAP",
    "summary": "Mobile interface to make purchases",
    "category": "Tools",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "maintainers": ["legalsylvain"],
    "depends": [
        "purchase",
        "mobile_kiosk_abstract",
        # OCA
        "product_supplierinfo_qty_multiplier",
    ],
    "data": [
        "views/templates.xml",
        "data/mobile_kiosk_application.xml",
    ],
    "qweb": [
        "static/src/xml/mobile_kiosk_purchase.xml",
    ],
    "installable": True,
}
