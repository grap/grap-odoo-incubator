from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.map_values(
        env.cr,
        openupgrade.get_legacy_name("state"),
        "state",
        [("confirm", "in_progress")],
        table="stock_inventory",
    )
