# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Jean-Sébastien SUZANNE (js@hashbang.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Point of Sale - Sectors",
    "summary": "Set Sectors to the products and display in given PoS Sessions",
    "version": "16.0.1.1.5",
    "category": "Point of Sale",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["point_of_sale"],
    "data": [
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "views/view_pos_sector.xml",
        "views/view_product_template.xml",
        "views/view_pos_config.xml",
        "views/view_res_config_settings.xml",
        "views/menu.xml",
    ],
    "demo": [
        "demo/pos_sector.xml",
        "demo/product_product.xml",
    ],
    "installable": True,
}
