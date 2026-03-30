# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Picking Account Move",
    "version": "16.0.1.2.1",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "stock_account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking.xml",
        "views/stock_picking_type.xml",
        "views/view_stock_picking_mass_generate_wizard.xml",
    ],
    "installable": True,
}
