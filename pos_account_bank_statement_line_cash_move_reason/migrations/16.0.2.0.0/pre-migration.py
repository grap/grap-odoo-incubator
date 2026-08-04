# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin Dupont
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    _logger.info("Try to fix weird bug...")
    openupgrade.logged_query(
        env.cr,
        """
    DELETE
        FROM ir_ui_view
        WHERE id in  (
            SELECT res_id
            FROM ir_model_data
            WHERE module = 'pos_account_bank_statement_line_cash_move_reason'
            AND model = 'ir.ui.view'
        );
    """,
    )
    _logger.info("=== Set onchange values produce_delay_in_hour")
    openupgrade.logged_query(
        env.cr,
        """
    DELETE
        FROM ir_model_data
        WHERE module = 'pos_account_bank_statement_line_cash_move_reason'
        AND model = 'ir.ui.view';

    """,
    )
