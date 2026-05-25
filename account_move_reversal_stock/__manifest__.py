# Copyright (C) 2026 - Today: GRAP (https://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Move Reversal Stock",
    "summary": "Facilitates the link between customer and inventory management.",
    "version": "16.0.1.1.0",
    "category": "Account",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "account",
        "stock",
        # OCA
        "stock_picking_invoice_link",
        "web_notify",
    ],
    "data": [
        "views/view_account_move.xml",
    ],
    "installable": True,
}
