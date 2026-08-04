# Copyright (C) 2025-Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)..
{
    "name": "Sale - Picking Quick Confirm",
    "version": "16.0.2.0.0",
    "category": "Stock",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "author": "GRAP",
    "maintainers": ["quentinDupont"],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        # Odoo
        "sale",
        # OCA
        "confirmation_wizard",
        # GRAP
        "stock_picking_quick_quantity_done",
    ],
    "data": ["views/view_sale_order.xml"],
}
