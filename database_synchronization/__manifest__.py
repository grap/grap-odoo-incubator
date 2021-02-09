# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Database Synchronization",
    "summary": "Synchronize many Odoo databases (datas, ...)",
    "version": "12.0.1.0.1",
    "category": "Settings",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "base",
    ],
    "external_dependencies": {
        "python": ["odoorpc"],
    },
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "data/ir_config_parameter.xml",
        "views/menu.xml",
        "views/view_synchronization_data.xml",
        "views/view_synchronization_mapping.xml",
    ],
    "installable": True,
}
