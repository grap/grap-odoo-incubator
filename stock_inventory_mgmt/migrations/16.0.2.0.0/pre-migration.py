from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.copy_columns(
        env.cr,
        {"stock_inventory": [("state", None, None)]},
    )
