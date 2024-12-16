# Copyright 2024 GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "User Limited Access Settings",
    "summary": """Create a new Administration group with
    limited access to create only users and companies""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "depends": [
        # Odoo
        "base_setup",
        "auth_signup",
        # OCA
        "base_user_role",
        "res_company_category",
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
    ],
    "demo": [
        "demo/res_partner.xml",
        "demo/res_users.xml",
    ],
}
