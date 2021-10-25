# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Point of Sale - Sectors",
    "summary": "Set Sectors to the products and display in given PoS Sessions",
    "version": "12.0.1.1.3",
    "category": "Point of Sale",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
    ],
    "data": [
        "security/ir_rule.xml",
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/view_pos_sector.xml",
        "views/view_product_template.xml",
        "views/view_pos_config.xml",
        "views/menu.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/pos_sector.xml",
        "demo/pos_config.xml",
        "demo/product_product.xml",
    ],
    "images": [
        "static/description/pos_config_form.png",
        "static/description/product_form.png",
    ],
    "installable": True,
}
