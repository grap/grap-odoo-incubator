# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import random
from datetime import datetime

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


def _create_sequence(env, name, code, prefix, padding, company_id):
    _logger.info("[stock_internal_use_of_products] create sequence : " + name)
    return env["ir.sequence"].create(
        {
            "name": name,
            "code": code,
            "prefix": prefix,
            "padding": padding,
            "company_id": company_id or False,
        }
    )


def _internal_use_cases_to_stock_picking_types(env):
    use_cases = env["internal.use.case"].search([])
    for use_case in use_cases:
        _company = use_case.company_id
        _prefix = str(
            _company.name[0:3].upper()
            + "/"
            + use_case.name[0:3].upper()
            + str(random.randint(0, 99))
            + "/%(year)s/"
        )
        seq = _create_sequence(
            env,
            str("Sequence for " + use_case.name),
            "stock.picking.type",
            _prefix,
            5,
            _company.id,
        )
        _logger.info(
            "[stock_internal_use_of_products] create Picking Type : " + use_case.name
        )
        if use_case.default_location_dest_id.usage == "internal":
            _code = "internal"
        elif use_case.default_location_dest_id.usage == "supplier":
            _code = "vendors"
        else:
            _code = "outgoing"
        env["stock.picking.type"].create(
            {
                "name": use_case.name,
                "sequence_id": seq.id,
                "code": _code,
                "default_location_src_id": use_case.default_location_src_id.id,
                "default_location_dest_id": use_case.default_location_dest_id.id,
                "journal_id": use_case.journal_id.id,
                "account_id": use_case.account_id.id,
            }
        )


def _get_stock_picking_type_from_use_case(env, use_case_name, company_id):
    return env["stock.picking.type"].search(
        [("name", "=", use_case_name), ("warehouse_id.company_id", "=", company_id)],
        limit=1,
    )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    # Create all Stock Picking Type
    _internal_use_cases_to_stock_picking_types(env)

    internal_uses = env["internal.use"].search([])
    for internal_use in internal_uses:
        # Find right new stock.picking.type
        _use_case = internal_use.internal_use_case_id
        _picking_type = _get_stock_picking_type_from_use_case(
            env, _use_case.name, _use_case.company_id.id
        )

        # Create picking
        _picking = env["stock.picking"].create(
            {
                "location_id": _picking_type.default_location_src_id.id,
                "location_dest_id": _picking_type.default_location_dest_id.id,
                "picking_type_id": _picking_type.id,
            }
        )

        # Set basic fields
        _date_done = datetime(
            internal_use.date_done.year,
            internal_use.date_done.month,
            internal_use.date_done.day,
        )
        _picking.update({"scheduled_date": _date_done})
        _picking.update({"note": internal_use.description})

        # Link internal use stock_move and move_lines to new stock picking
        _moves = internal_use.stock_move_ids
        _moves_lines = _moves.mapped("move_line_ids")
        _picking.update({"move_ids_without_package": [(6, 0, _moves.ids)]})
        _picking.update({"move_line_ids": [(6, 0, _moves_lines.ids)]})

        _logger.info(
            "[stock_internal_use_of_products] create Picking : " + _picking.name
        )

        # Handle state, account_move, account_move_state
        if internal_use.state == "draft":
            _state = "draft"
            if internal_use.internal_use_case_id.journal_id:
                _account_move_state = "waiting"
            else:
                _account_move_state = "no_need"

        elif internal_use.state in "confirmed":
            _state = "done"
            _account_move_state = "to_do"

        elif internal_use.state in "done":
            _state = "done"
            # Link account_move
            if internal_use.account_move_id:
                _account_move_state = "done"
                _picking.update({"account_move_id": internal_use.account_move_id.id})
            else:
                _account_move_state = "to_do"
        else:
            _logger.error(
                "[stock_internal_use_of_products] Internal use has uncoinsistent state"
            )

        _picking.update({"account_move_state": _account_move_state})
        _picking.update({"state": _state})
