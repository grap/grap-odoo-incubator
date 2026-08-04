# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Down Payment Products per Company",
    "summary": "Handle Down Payment products per company and tax",
    "version": "16.0.2.0.0",
    "category": "Sale",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain", "quentinDupont"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": ["sale"],
    "data": [
        "wizards/view_sale_advance_payment_inv.xml",
        "views/view_res_config_settings.xml",
    ],
    "demo": [
        "demo/demo_account_tax.xml",
        "demo/demo_product_product.xml",
        "demo/demo_res_company.xml",
    ],
    "installable": True,
}
