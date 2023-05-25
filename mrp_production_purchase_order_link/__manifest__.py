# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Purchase UX",
    "summary": "Module to help user when using MRP and Purchase",
    "version": "12.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "purchase",
        # OCA modules
        "web_notify",
    ],
    "data": [
        "views/view_mrp_production.xml",
    ],
    "installable": True,
}
