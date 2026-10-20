# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mobile Kiosk Purchase",
    "version": "16.0.1.0.0",
    "author": "GRAP",
    "summary": "Mobile interface to make purchases",
    "category": "Tools",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "maintainers": ["legalsylvain"],
    "depends": [
        # Odoo
        "purchase",
        # OCA
        "product_supplierinfo_qty_multiplier",
        "product_main_seller",
        "partner_manual_rank",
        # GRAP
        "mobile_kiosk_abstract",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/mobile_kiosk_application.xml",
        "views/view_res_partner.xml",
        "views/view_product_product.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mobile_kiosk_purchase/static/src/PurchaseAction/**/*",
            "mobile_kiosk_purchase/static/src/SetSupplier/**/*",
            "mobile_kiosk_purchase/static/src/SetProduct/**/*",
            "mobile_kiosk_purchase/static/src/SetQuantity/**/*",
        ],
    },
    "demo": [
        "demo/product_supplierinfo.xml",
        "demo/res_partner.xml",
    ],
    "installable": True,
}
