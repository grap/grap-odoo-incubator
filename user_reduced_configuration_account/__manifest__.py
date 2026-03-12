# Copyright 2024 GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "User - Reduced Configuration (Account)",
    "summary": """Glue module to allow users to have limited access
    to configuration elements, when account is installed.""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "depends": ["user_reduced_configuration", "account"],
    "demo": ["demo/reduced_configuration_line.xml"],
    "auto_install": True,
}
