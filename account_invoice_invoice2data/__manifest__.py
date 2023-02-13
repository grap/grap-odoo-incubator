# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Invoice - xxx",
    "version": "12.0.1.0.1",
    "category": "Product",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["account"],
    "data": [
        "views/view_account_invoice.xml",
        "wizards/wizard_invoice2data_import.xml",
    ],
    "external_dependencies": {"python": ["invoice2data"]},
    "demo": [
        "demo/res_partner.xml",
        "demo/product_product.xml",
    ],
    "installable": True,
}
