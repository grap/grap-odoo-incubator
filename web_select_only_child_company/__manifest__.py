# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Companies - Only Childs",
    "summary": "When selecting a company,"
    " automatically select all the child companies.",
    "version": "16.0.1.0.1",
    "category": "Tools",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["web"],
    "assets": {
        "web.assets_backend": [
            "web_select_only_child_company/static/src/xml/switch_company_menu.xml",
            "web_select_only_child_company/static/src/js/switch_company_menu.esm.js",
        ],
    },
    "demo": ["demo/res_company.xml"],
    "installable": True,
}
