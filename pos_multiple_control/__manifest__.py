# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Point Of Sale - Multiple Cash Control",
    "summary": "Allow user to control each statement and add extra checks",
    "version": "12.0.1.0.0",
    "category": "Point of Sale",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "license": "AGPL-3",
    "depends": ["point_of_sale", "pos_cash_move_reason",],
    "data": [
        "views/view_account_journal.xml",
        "views/view_pos_config.xml",
        "views/view_pos_session.xml",
        "wizard/wizard_pos_update_statement_balance.xml"
    ],
    "images": [
        "static/description/pos_session_closing_form.png",
        "static/description/account_bank_statement_piece_form.png",
        "static/description/account_bank_statement_summary_form.png",
        "static/description/account_journal_bank_setting.png",
    ],
    "demo": [],
    "installable": True,
}