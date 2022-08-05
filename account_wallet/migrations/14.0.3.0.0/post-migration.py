# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.cr.execute(
        """
        SELECT value
        FROM ir_config_parameter
        WHERE key='account_move_credit_notes_wallet_default_product'
        """
    )
    result = env.cr.fetchall()
    if result:
        product_id = int(result[0][0])
        env.cr.execute(
            """UPDATE account_wallet_type
            SET credit_note_product_id = %s
            """,
            (product_id,),
        )
        env.cr.execute(
            """
            DELETE
            FROM ir_config_parameter
            WHERE key='account_move_credit_notes_wallet_default_product';
            """
        )
