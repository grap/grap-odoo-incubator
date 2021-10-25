# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Deposit Product per Company",
    "summary": "Handle one deposit product (down payment) per company",
    "version": "12.0.1.1.0",
    "category": "Sale",
    "author": "GRAP, Odoo Community Association (OCA)",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "sale",
    ],
    "data": [
        "views/view_res_company.xml",
    ],
    "installable": True,
}
