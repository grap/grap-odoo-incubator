# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL
# Notes: Some files comes from Odoo CE V12. Copyright: Odoo SA (see headers)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock Inventory",
    "summary": "Port and improve missing stock inventory features for"
    " previous odoo versions. (12.0, etc.)",
    "version": "16.0.2.0.0",
    "category": "Usability",
    "license": "AGPL-3",
    "author": "GRAP",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "depends": [
        "stock",
        # OCA
        "product_compute_template_field_from_variant_helper",
        "report_xlsx_helper",
    ],
    "excludes": ["stock_inventory"],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/view_stock_inventory_line.xml",
        "views/view_stock_inventory.xml",
        "views/view_stock_racking.xml",
        "views/view_product_template.xml",
        "views/view_product_product.xml",
        "wizards/view_wizard_stock_inventory_merge.xml",
        "reports/report_stock_inventory_qweb.xml",
        "reports/ir_actions_report.xml",
    ],
    "demo": [
        "demo/stock_racking.xml",
        "demo/product_product.xml",
        "demo/stock_inventory.xml",
    ],
    "installable": True,
}
