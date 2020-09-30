# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Mobile Kiosk Purchase",
    "version": "12.0.1.0.2",
    "author": "GRAP",
    "summary": "Mobile interface to make purchases",
    "category": "Tools",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "mobile_kiosk_abstract",
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
