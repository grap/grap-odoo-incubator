# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Point of Sale - Odoo POS Driver",
    "summary": "Adapt Odoo Point of sale when using odoo-pos-driver"
    " instead of pywebdriver (or IoT Box)",
    "version": "12.0.1.0.0",
    "category": "Point of Sale",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["point_of_sale"],
    "data": [
        "views/assets.xml",
        "views/view_pos_config.xml",
    ],
    "demo": ["demo/pos_config.xml"],
    "installable": True,
}
