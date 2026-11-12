# Copyright (C) 2026 - Today: GRAP (https://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def migrate(env, version):
    # Fill database for migrated datas from Internal Use
    _logger.info(
        "[stock_picking_valuation] Stock Pickings : compute total valuation ..."
    )
    openupgrade.logged_query(
        env.cr,
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
        """,
    )
