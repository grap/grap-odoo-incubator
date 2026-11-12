# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Avoid computation of fields, because values will be wrong
    # in the past, due to the fact that standard_price is not known
    # for old stock moves.
    if not openupgrade.column_exists(env.cr, "stock_move", "unit_valuation"):
        openupgrade.add_columns(env, [("stock.move", "unit_valuation", "float", 0.0)])

    if not openupgrade.column_exists(env.cr, "stock_move", "total_valuation"):
        openupgrade.add_columns(env, [("stock.move", "total_valuation", "float", 0.0)])

    if not openupgrade.column_exists(env.cr, "stock_picking", "total_valuation"):
        openupgrade.add_columns(
            env, [("stock.picking", "total_valuation", "float", 0.0)]
        )
