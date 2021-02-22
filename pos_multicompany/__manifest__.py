# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Point Of Sale - Multi Company",
    "version": "12.0.1.0.1",
    "summary": "Point of Sale Settings in Multi company context",
    "category": "Point of Sale",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
    ],
    "data": [
        "security/ir_rule.xml",
        "views/view_pos_config.xml",
        "views/view_pos_session.xml",
        "views/view_pos_order.xml",
        "views/view_pos_category.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
    ],
    "images": [
        "static/description/pos_category_tree.png",
    ],
    "installable": True,
}
