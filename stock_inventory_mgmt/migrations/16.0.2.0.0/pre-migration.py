from openupgradelib import openupgrade

from odoo.tools.sql import column_exists


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.copy_columns(
        env.cr,
        {"stock_inventory": [("state", None, None)]},
    )

    if column_exists(env.cr, "stock_inventory", "partner_id"):
        openupgrade.rename_columns(
            env.cr, {"stock_inventory": [("partner_id", "owner_id")]}
        )

    if column_exists(env.cr, "stock_inventory_line", "partner_id"):
        openupgrade.rename_columns(
            env.cr, {"stock_inventory_line": [("partner_id", "owner_id")]}
        )
