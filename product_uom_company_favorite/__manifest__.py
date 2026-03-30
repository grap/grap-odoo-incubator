# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product UoM - Company Favorites",
    "summary": "Possilibity to set favorite product units" " of Measure per company",
    "version": "16.0.1.0.3",
    "category": "Product",
    "author": "GRAP,Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "views/view_uom_uom.xml",
        "views/view_uom_category.xml",
        "views/view_product_template.xml",
    ],
    "demo": ["demo/res_company.xml"],
    "installable": True,
    "post_init_hook": "initialize_is_favorite_field",
}
