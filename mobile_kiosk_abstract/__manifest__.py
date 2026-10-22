# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mobile Kiosk Abstract",
    "version": "16.0.1.1.0",
    "author": "GRAP",
    "summary": "Abstract Module that provides a framework to develop"
    " 'kiosk application' for mobile usage like in 'hr_attendance'"
    " Odoo module",
    "category": "Tools",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "maintainers": ["legalsylvain"],
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/view_mobile_kiosk_application.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mobile_kiosk_abstract/static/src/AbstractAction/**/*",
            "mobile_kiosk_abstract/static/src/PadWidget/**/*",
            "mobile_kiosk_abstract/static/src/scss/**/*",
        ],
    },
    "demo": [
        "demo/res_partner.xml",
        "demo/product_product.xml",
        "demo/product_supplierinfo.xml",
    ],
    "installable": True,
}
