# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Point of Sale - Wallet",
    "version": "12.0.1.0.1",
    "category": "Point Of Sale",
    "summary": "Handle wallet in the point of sale. (check and display amount)",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
        "account_wallet",
    ],
    "data": [
        "views/assets.xml",
        "views/view_account_journal.xml",
    ],
    "qweb": [
        "static/src/xml/pos_wallet.xml",
    ],
    "auto_installable": True,
}
