# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Stock - Internal Use of products",
    "summary": "Declare the use of products for specific uses (eg: gifts,...)",
    "version": "12.0.1.1.4",
    "category": "Stock",
    "author": "GRAP",
    "website": "https://github.com/OCA/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["stock_account",],
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "data/ir_sequence.xml",
        "views/view_internal_use.xml",
        "views/view_internal_use_line.xml",
        "views/view_internal_use_case.xml",
        "views/view_internal_use_mass_generate_wizard.xml",
    ],
    "demo": [
        "demo/account_account.xml",
        "demo/account_journal.xml",
        "demo/account_tax.xml",
        "demo/product_product.xml",
        "demo/res_groups.xml",
        "demo/internal_use_case.xml",
        "demo/internal_use.xml",
    ],
    "images": [
        "static/description/internal_use_form.png",
        "static/description/internal_use_case_form.png",
    ],
    "installable": True,
}
