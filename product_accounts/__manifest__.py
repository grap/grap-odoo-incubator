# Copyright 2024 GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product - Accounting Settings",
    "summary": """Compute and display income - expense account
    at product level""",
    "version": "16.0.1.0.2",
    "license": "AGPL-3",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "depends": ["account"],
    "data": [
        "views/view_product_template.xml",
        "views/view_product_product.xml",
    ],
}
