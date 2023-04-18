# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Database Synchronization",
    "summary": "Synchronize many Odoo Databases (datas, ...)",
    "version": "12.0.2.2.4",
    "category": "Settings",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "queue_job",
    ],
    "external_dependencies": {
        "python": ["odoorpc"],
    },
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "data/ir_config_parameter.xml",
        "data/queue_job_channel.xml",
        "data/queue_job_function.xml",
        "views/menu.xml",
        "views/view_synchronization_mapping.xml",
        "views/view_synchronization_data.xml",
    ],
    "demo": [
        "demo/synchronization_data.xml",
    ],
    "installable": True,
}
