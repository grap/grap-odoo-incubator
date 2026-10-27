# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


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

    # Fill database for migrated datas from Internal Use
    _logger.info(
        "[stock_picking_valuation] Stock Pickings : compute total valuation ..."
    )
    cr.execute(
        """
        UPDATE stock_picking AS picking
        SET total_valuation =
        CASE
            WHEN picking.location_id = picking_type.default_location_src_id
                AND picking.location_dest_id = picking_type.default_location_dest_id
            THEN move_values.total_valuation

            WHEN picking.location_id = picking_type.default_location_dest_id
                AND picking.location_dest_id = picking_type.default_location_src_id
            THEN -move_values.total_valuation

            ELSE 0
        END
        FROM stock_picking_type AS picking_type,
             (
                SELECT move.picking_id, SUM(move.total_valuation) AS total_valuation
                FROM stock_move AS move
                GROUP BY move.picking_id
             ) AS move_values
        WHERE picking.picking_type_id = picking_type.id
          AND move_values.picking_id = picking.id
    """
    )
