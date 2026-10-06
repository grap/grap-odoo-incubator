# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL
# Notes: Some files comes from Odoo CE V12. Copyright: Odoo SA (see headers)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Inventory",
    "summary": "Port and improve missing stock inventory features for"
    " previous odoo versions. (12.0, etc.)",
    "version": "16.0.1.0.0",
    "category": "Usability",
    "license": "LGPL-3",
    "author": "GRAP",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/view_stock_inventory_line.xml",
        "views/view_stock_inventory.xml",
    ],
    "installable": True,
}
