# Copyright 2024 GRAP
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "User - Reduced Configuration",
    "summary": """Allow user to have limited access to configuration elements""",
    "version": "16.0.3.0.0",
    "license": "AGPL-3",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "depends": ["base_setup"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/view_res_reduced_config_settings.xml",
        "views/view_reduced_configuration.xml",
        "views/menu.xml",
    ],
    "demo": [
        "demo/res_partner.xml",
        "demo/res_users.xml",
        "demo/reduced_configuration.xml",
    ],
}
