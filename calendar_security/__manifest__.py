# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Calendar Security",
    "summary": "Add a group to display 'Calendar' Application menu entry",
    "version": "16.0.1.0.0",
    "category": "Usability",
    "license": "AGPL-3",
    "author": "GRAP",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "depends": ["calendar"],
    "data": [
        "security/res_groups.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
