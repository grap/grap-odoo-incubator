# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Picking Report Summary",
    "summary": "Stock Picking Report Summary",
    "version": "13.0.1.0.1",
    "author": "GRAP, " "Odoo Community Association (OCA)",
    "maintainers": ["quentinDupont"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "category": "Warehouse Management",
    "license": "AGPL-3",
    "depends": ["stock",],
    "data": [
        "reports/report_paperformat.xml",
        "reports/report_print_picking_summary.xml",
        "reports/report_print_picking_summary_template.xml",
        "views/view_picking_summary_wizard.xml",
        "views/action.xml",
    ],
    "installable": True,
}
