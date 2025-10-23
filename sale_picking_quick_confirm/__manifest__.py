# Copyright (C) 2025-Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)..
{
    "name": "Sale Picking Quick Confirm",
    "version": "16.0.1.1.1",
    "category": "Stock",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "author": "GRAP, " "Odoo Community Association (OCA)",
    "maintainers": [
        "quentinDupont",
    ],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_management",
        "stock",
    ],
    "data": [
        "views/view_sale_order.xml",
    ],
}
