# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Point Of Sale - Multiple Cash Control',
    'summary': "Allow user to control each statement and add extra checks",
    'version': '8.0.3.0.0',
    'category': 'Point of Sale',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'point_of_sale',
        'pos_cash_move_reason',
    ],
    'data': [
        'views/view_pos_box.xml',
        'views/view_account_journal.xml',
        'views/view_pos_session.xml',
        'views/view_pos_session_opening.xml',
    ],
    'images': [
        'static/description/pos_session_closing_form.png',
        'static/description/account_bank_statement_piece_form.png',
        'static/description/account_bank_statement_summary_form.png',
        'static/description/account_journal_bank_setting.png',
    ],
    'demo': [
        'demo/res_groups.xml',
        'demo/account_journal.xml',
        'demo/pos_config.xml',
    ],
    'installable': False,
}
