# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import random
from datetime import datetime

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def _create_sequence(env, name, code, prefix, padding, company_id):
    _logger.info("[stock_picking_account_move] create sequence : " + name)
    return env["ir.sequence"].create(
        {
            "name": name,
            "code": code,
            "prefix": prefix,
            "padding": padding,
            "company_id": company_id or False,
        }
    )


def fetchall_dict(cr):
    columns = [col[0] for col in cr.description]
    return [dict(zip(columns, row)) for row in cr.fetchall()]  # noqa: B905


def _internal_use_cases_to_stock_picking_types(env):
    ResCompany = env["res.company"]
    StockLocation = env["stock.location"]
    env.cr.execute(
        """
        SELECT * from internal_use_case;
        """
    )
    use_cases = fetchall_dict(env.cr)

    for use_case in use_cases:
        _company_id = use_case.get("company_id")
        _company = ResCompany.browse(_company_id)
        _use_case_name = use_case.get("name")
        _prefix = str(
            _company.name[0:3].upper()
            + "/"
            + use_case.get("name")[0:3].upper()
            + str(random.randint(0, 99))
            + "/%(year)s/"
        )
        seq = _create_sequence(
            env,
            str("Sequence for " + _use_case_name),
            "stock.picking.type",
            _prefix,
            5,
            _company_id,
        )
        _logger.info(
            "[stock_picking_account_move] create Picking Type : " + _use_case_name
        )
        location_src = StockLocation.browse(use_case.get("default_location_src_id"))
        location_dest = StockLocation.browse(use_case.get("default_location_dest_id"))
        env["stock.picking.type"].create(
            {
                "name": use_case.get("name"),
                "company_id": _company.id,
                "sequence_id": seq.id,
                "sequence_code": _prefix,
                "code": "internal",
                "default_location_src_id": location_src.id,
                "default_location_dest_id": location_dest.id,
                "journal_id": use_case.get("journal_id"),
                "account_id": use_case.get("account_id"),
            }
        )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    # Create all Stock Picking Type
    _logger.info(
        "[stock_picking_account_move] MIGRATION from stock_internal_use_of_products"
    )
    _internal_use_cases_to_stock_picking_types(env)

    env.cr.execute(
        """
        SELECT * from internal_use;
        """
    )
    internal_uses = fetchall_dict(env.cr)

    for internal_use in internal_uses:
        # Find right new stock.picking.type
        env.cr.execute(
            """
            SELECT
                spt.*
            FROM internal_use_case AS iuc
            JOIN internal_use iu
                ON iuc.id = iu.internal_use_case_id
            JOIN stock_picking_type spt
                ON spt.name->>'en_US' = iuc.name
            WHERE iu.id = %s
            LIMIT 1
            """,
            (internal_use["id"],),
        )
        columns = [col[0] for col in env.cr.description]
        _picking_type = [dict(zip(columns, row)) for row in env.cr.fetchall()]  # noqa: B905

        # Create picking
        _picking = env["stock.picking"].create(
            {
                "location_id": _picking_type[0].get("default_location_src_id"),
                "location_dest_id": _picking_type[0].get("default_location_dest_id"),
                "picking_type_id": _picking_type[0].get("id"),
            }
        )

        # Set basic fields
        _date_done = datetime(
            internal_use.get("date_done").year,
            internal_use.get("date_done").month,
            internal_use.get("date_done").day,
        )
        _picking.write(
            {
                "date_done": _date_done,
                "note": internal_use.get("description"),
            }
        )

        # Link internal use stock_move and move_lines to new stock picking
        env.cr.execute(
            """
            SELECT *
            FROM stock_move
            WHERE internal_use_id = %s
            """,
            (internal_use["id"],),
        )
        _moves = fetchall_dict(env.cr)
        move_ids = [row["id"] for row in _moves]
        move_records = env["stock.move"].browse(move_ids)
        move_line_records = move_records.mapped("move_line_ids")

        _picking.update(
            {
                "move_ids_without_package": [(6, 0, move_ids)],
                "move_line_ids": [(6, 0, move_line_records.ids)],
            }
        )

        _logger.info("[stock_picking_account_move] create Picking : " + _picking.name)

        # Handle state, account_move, account_move_state
        env.cr.execute(
            """
            SELECT *
            FROM internal_use_case
            WHERE id = %s
            LIMIT 1
            """,
            (internal_use["internal_use_case_id"],),
        )

        internal_use_case = fetchall_dict(env.cr)[0]

        if internal_use.get("state") == "draft":
            _state = "draft"
            if internal_use_case.get("journal_id"):
                _account_move_state = "waiting"
            else:
                _account_move_state = "no_need"

        elif internal_use.get("state") in "confirmed":
            _state = "done"
            _account_move_state = "to_do"

        elif internal_use.get("state") in "done":
            _state = "done"
            # Link account_move
            if internal_use.get("account_move_id"):
                _account_move_state = "done"
                _picking.update(
                    {"account_move_id": internal_use.get("account_move_id")}
                )
            else:
                _account_move_state = "to_do"
        else:
            _logger.error(
                "[stock_picking_account_move] Internal use has uncoinsistent state"
            )

        _picking.write(
            {
                "account_move_state": _account_move_state,
                "state": _state,
            }
        )
