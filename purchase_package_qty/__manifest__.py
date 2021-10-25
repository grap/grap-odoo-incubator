# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase - Package Quantity",
    "version": "12.0.1.1.1",
    "category": "Purchase",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "purchase",
    ],
    "data": [
        "views/view_product_supplierinfo.xml",
    ],
    "demo": [
        "demo/res_groups.xml",
        "demo/product_template.xml",
        "demo/product_supplierinfo.xml",
        "demo/purchase_order.xml",
    ],
    "installable": True,
}
