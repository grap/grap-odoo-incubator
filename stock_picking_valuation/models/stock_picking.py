# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (sylvain.legal@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    direction_type = fields.Selection(
        selection=[
            ("undefined", "Undefined Direction"),
            ("correct", "Correct Direction"),
            ("opposite", "Opposite Direction"),
        ],
        compute="_compute_direction_type",
        help="If checked, mention that the picking has the opposition"
        " direction, relative to the direction of the picking type.",
    )

    total_valuation = fields.Float(
        digits="Product Price",
        compute="_compute_total_valuation",
        store=True,
    )

    @api.depends(
        "picking_type_id.default_location_src_id",
        "picking_type_id.default_location_dest_id",
        "location_id",
        "location_dest_id",
    )
    def _compute_direction_type(self):
        for picking in self:
            if (
                picking.location_id == picking.picking_type_id.default_location_src_id
                and picking.location_dest_id
                == picking.picking_type_id.default_location_dest_id
            ):
                picking.direction_type = "correct"
            elif (
                picking.location_id == picking.picking_type_id.default_location_dest_id
                and picking.location_dest_id
                == picking.picking_type_id.default_location_src_id
            ):
                picking.direction_type = "opposite"
            else:
                picking.direction_type = "undefined"

    @api.depends(
        "move_ids.total_valuation",
        "picking_type_id.default_location_src_id",
        "picking_type_id.default_location_dest_id",
        "location_id",
        "location_dest_id",
    )
    def _compute_total_valuation(self):
        for picking in self:
            direction_type = picking.direction_type
            if direction_type == "correct":
                picking.total_valuation = sum(
                    picking.mapped("move_ids.total_valuation")
                )
            elif direction_type == "opposite":
                picking.total_valuation = -sum(
                    picking.mapped("move_ids.total_valuation")
                )
            else:
                picking.total_valuation = 0
