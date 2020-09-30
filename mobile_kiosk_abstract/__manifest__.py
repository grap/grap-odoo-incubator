# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mobile Kiosk Abstract",
    "version": "12.0.1.0.2",
    "author": "GRAP",
    "summary": "Mobile Kiosk Absract Module",
    "category": "Tools",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/templates.xml",
        "views/view_product_product.xml",
        "views/view_res_partner.xml",
        "views/view_mobile_kiosk_application.xml",
    ],
    "qweb": [
        "static/src/xml/mobile_kiosk_abstract.xml",
    ],
    "demo": [
        "demo/res_partner.xml",
        "demo/product_product.xml",
        "demo/product_supplierinfo.xml",
    ],
    "installable": True,
}
