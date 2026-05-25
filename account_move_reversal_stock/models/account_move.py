# Copyright 2026-Today: GRAP (https://www.grap.coop)
# Copyright Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    stock_picking_could_be_returned = fields.Boolean(
        compute="_compute_stock_picking_could_be_returned"
    )

    @api.depends("move_type", "state", "picking_ids", "invoice_line_ids")
    def _compute_stock_picking_could_be_returned(self):
        for move in self:
            move.stock_picking_could_be_returned = False
            pickings = move.picking_ids

            if (
                not pickings
                or move.state in ("draft", "cancel")
                or move.move_type not in ("out_invoice", "out_refund")
            ):
                continue

            # Check if return StockPicking exists
            stock_moves = pickings.mapped("move_ids")
            has_return = any(m.origin_returned_move_id for m in stock_moves)

            ### For Customer Invoice
            if move.move_type == "out_invoice":
                sale_orders = move.invoice_line_ids.mapped("sale_line_ids.order_id")
                if not sale_orders:
                    continue

                invoices = sale_orders.mapped("invoice_ids")
                others = invoices.filtered(
                    lambda inv, move_id=move.id: inv.id != move_id
                )
                has_refund = any(inv.move_type == "out_refund" for inv in others)

                # Invoice created through refund 'modify' flow
                if has_refund:
                    move.stock_picking_could_be_returned = not has_return

            ### For Credit Note
            elif move.move_type == "out_refund":
                move.stock_picking_could_be_returned = not has_return

    # This function uses StockReturnPicking wizard, it handle two cases :
    #      Credit Note → return theses quantities
    #      New Invoice through 'modify' refund flow → return quantity differentials
    def reverse_stock_picking(self):
        StockReturnPicking = self.env["stock.return.picking"]
        for move in self:
            pickings = move.picking_ids
            for picking in pickings:
                wiz = StockReturnPicking.with_context(
                    **{
                        "active_id": picking.id,
                        "active_ids": [picking.id],
                        "active_model": "stock.picking",
                    }
                ).create({})
                wiz._onchange_picking_id()

                res = wiz.create_returns()
                pick_return = self.env["stock.picking"].browse(res["res_id"])

                for return_move in pick_return.move_ids:
                    origin_move = return_move.origin_returned_move_id

                    res_line = move.invoice_line_ids.filtered(
                        lambda line, rsm_product=return_move.product_id: line.product_id
                        == rsm_product
                    )
                    if res_line:
                        if move.move_type in ("out_refund"):
                            # Credit Note → return theses new quantities
                            return_move.product_uom_qty = res_line[0].quantity
                        elif move.move_type in ("out_invoice"):
                            # New Invoice through 'modify' refund flow
                            # E.g Original Invoice : 3 bananas
                            # New Editable Invoice : 2 bananas
                            #   → need to return 1 in StockReturnPicking
                            return_move.product_uom_qty -= res_line[0].quantity

                        return_move.quantity_done = return_move.product_uom_qty

                    # Link new picking return Invoice thanks to stock_move invoice lines
                    return_move.invoice_line_ids = [
                        (6, 0, origin_move.invoice_line_ids.ids)
                    ]

                pick_return.with_context(skip_backorder=True).button_validate()

                self.env.user.notify_success(
                    message=_("New Return Picking: %(name)s")
                    % {"name": pick_return.name}
                )

        return True
