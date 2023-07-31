# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Production Purchase Order Link",
    "summary": "This module adds a smart button in PO and MO to link them.",
    "version": "12.0.1.0.1",
    "category": "GRAP - incubator",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "mrp",
        "purchase_stock",
    ],
    "data": [
        "views/view_mrp_production.xml",
    ],
    "installable": True,
}
