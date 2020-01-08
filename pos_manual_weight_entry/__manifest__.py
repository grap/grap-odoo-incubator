# Copyright (C) 2015-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Point Of Sale - Manual Weight Entry",
    "summary": "Allow user to enter manualy the weight in the Point Of Sale",
    "version": "12.0.1.0.0",
    "category": "Point Of Sale",
    "author": "GRAP",
    "maintainers": ["legalsylvain"],
    "website": "https://www.github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["pos_tare"],
    "data": ["views/assets.xml"],
    "qweb": ["static/src/xml/pos_manual_weight_entry.xml"],
    "installable": True,
    "images": ["static/description/pos_manual_weight_entry.png"],
}
