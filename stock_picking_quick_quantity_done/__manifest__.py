# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)..
{
    "name": "Stock Picking Quick Quantity Done",
    "version": "12.0.1.1.0",
    "category": "Stock",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "author": "GRAP, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
        "stock",
    ],
    "data": [
        "views/view_stock_picking.xml",
    ],
}
