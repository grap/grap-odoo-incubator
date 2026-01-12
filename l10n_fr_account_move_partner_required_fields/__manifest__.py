# Copyright (C) 2025 - Today: Quentin DUPONT (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "L10N FR Account Move Partner Required Fields",
    "version": "16.0.1.0.0",
    "category": "Custom",
    "author": "GRAP",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "depends": [
        "account",
        # OCA
        "l10n_fr_siret",
    ],
    "data": [
        "views/view_account_move.xml",
        "views/view_res_partner.xml",
    ],
}
