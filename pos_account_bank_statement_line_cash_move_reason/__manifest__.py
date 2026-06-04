# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "PoS Account Bank Statement Line - Cash Move Reason",
    "version": "16.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://github.com/grap/grap-odoo-incubator",
    "license": "AGPL-3",
    "author": "GRAP,Odoo Community Association (OCA)",
    "depends": [
        "pos_account_bank_statement_line",
        "pos_cash_move_reason",
    ],
    "data": [
        "views/account_bank_statement_line.xml",
    ],
    "auto_install": True,
}
