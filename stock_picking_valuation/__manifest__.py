# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Valuation",
    "version": "16.0.1.1.1",
    "category": "Stock",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["stock"],
    "external_dependencies": {"python": ["openupgradelib"]},
    "data": [
        "views/stock_move.xml",
        "views/stock_picking.xml",
    ],
    "pre_init_hook": "pre_init_hook",
}
