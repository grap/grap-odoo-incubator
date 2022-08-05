# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "account_wallet_type", "no_anonymous"):
        openupgrade.rename_columns(
            {"account_wallet_type": [("no_anonymous", "automatic_nominative_creation")]}
        )
