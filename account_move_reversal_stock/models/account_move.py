# Copyright 2026-Today: GRAP (https://www.grap.coop)
# Copyright Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    stock_picking_could_be_adjusted = fields.Boolean(
        compute="_compute_stock_picking_could_be_adjusted"
    )

    @api.depends("move_type", "state", "invoice_line_ids")
    def _compute_stock_picking_could_be_adjusted(self):
        """Display button for
        - Invoices in confirm State
        - when juste ONE quantity delivered != invoiced
        """
        for move in self:
            move.stock_picking_could_be_adjusted = False

            if move.state in ("draft", "cancel") or move.move_type not in (
                "out_invoice",
                "out_refund",
            ):
                continue
            else:
                for invoice_line in move.invoice_line_ids:
                    sale_line = invoice_line.sale_line_ids[:1]
                    if sale_line.qty_delivered != sale_line.qty_invoiced:
                        move.stock_picking_could_be_adjusted = True
                        break

    def _create_picking_and_move(
        self,
        account_move,
        picking_lines,
        is_return=False,
    ):
        """
        Intern function to create a Picking and its Moves
        linked with SO, WH and Invoice
        """
        StockPicking = self.env["stock.picking"]
        StockMove = self.env["stock.move"]

        first_picking = account_move.picking_ids[:1]

        if not first_picking:
            return False

        # Picking configuration : inverse locations for is_return
        if is_return:
            picking_type = (
                first_picking.picking_type_id.return_picking_type_id
                or first_picking.picking_type_id
            )
            picking_location_src = first_picking.location_dest_id
            picking_location_dest = first_picking.location_id
        else:
            picking_type = first_picking.picking_type_id
            picking_location_src = first_picking.location_id
            picking_location_dest = first_picking.location_dest_id

        picking_vals = {
            "picking_type_id": picking_type.id,
            "partner_id": account_move.partner_id.id,
            "origin": account_move.name,
            "move_type": "direct",
            "location_id": picking_location_src.id,
            "location_dest_id": picking_location_dest.id,
        }

        # 1 - Create Picking
        new_picking = StockPicking.create(picking_vals)

        # 2 - Create StockMoves
        for line in picking_lines:
            sale_line = line.get("sale_line")
            invoice_line = line.get("invoice_line")
            product = line["product_id"]
            quantity = line["quantity"]

            move_vals = {
                "name": sale_line.name,
                "product_id": product.id,
                "product_uom_qty": quantity,
                "product_uom": sale_line.product_uom.id,
                "location_id": picking_location_src.id,
                "location_dest_id": picking_location_dest.id,
                "picking_id": new_picking.id,
                "sale_line_id": sale_line.id,
                "group_id": sale_line.order_id.procurement_group_id.id,
                "description_picking": sale_line.name,
                # invoice_line_ids links with stock_move <> invoice
                "invoice_line_ids": [(6, 0, invoice_line.ids)],
            }

            # link stock_move and return stock_move
            if is_return:
                origin_stock_move = sale_line.move_ids[:1]

                if origin_stock_move:
                    move_vals.update(
                        {
                            "origin_returned_move_id": origin_stock_move.id,
                            # to_refund permits to adjust SO,
                            "to_refund": True,
                        }
                    )

            # Finally create it
            StockMove.create(move_vals)

        # Force transfer
        new_picking.action_confirm()
        new_picking.action_assign()
        new_picking.quick_quantities_done()
        new_picking.button_validate()

        self.env.user.notify_success(
            message=_("New Picking: %(name)s") % {"name": new_picking.name}
        )

        return True

    def adjust_stock_picking(self):
        """
        MAIN FUNCTION : Adjust Stock for three cases :
            CASE A : new product added on invoice
            CASE B : out_invoice: new invoice through 'modify' refund flow
                    → quantity adjustment
            CASE C : out_refund: credit note
                    → return theses quantities
        It follows stock_move and sale_order_line so it updates SO quantities
        """
        for move in self:
            move_type = move.move_type
            new_out_picking = []
            new_return_picking = []

            # === 1st STEP : Go through each AccountMove lines to fill
            #                new_out_picking and new_return_picking
            for invoice_line in move.invoice_line_ids:
                product = invoice_line.product_id

                # For sections and notes
                if not product:
                    continue

                sale_line = invoice_line.sale_line_ids[:1]

                # === CASE A : new product added
                if not sale_line:
                    # in New invoice
                    if move_type == "out_invoice" and invoice_line.quantity > 0:
                        new_out_picking.append(
                            {
                                "product_id": product,
                                "quantity": abs(invoice_line.quantity),
                                "sale_line": False,
                                "invoice_line": invoice_line,
                            }
                        )
                    # in Credit note
                    else:
                        new_return_picking.append(
                            {
                                "product_id": product,
                                "quantity": abs(invoice_line.quantity),
                                "sale_line": False,
                                "invoice_line": invoice_line,
                            }
                        )

                    continue

                # === CASE B : New Invoice
                if move_type == "out_invoice":
                    invoice_qty = invoice_line.quantity
                    delivered_qty = sale_line.qty_delivered
                    difference = invoice_qty - delivered_qty

                    if not difference:
                        continue

                    # === CASE B.1 : More invoiced
                    #     → need to transfer in new_out_picking
                    if difference > 0:
                        new_out_picking.append(
                            {
                                "product_id": product,
                                "quantity": abs(difference),
                                "sale_line": sale_line,
                                "invoice_line": invoice_line,
                            }
                        )

                    # === CASE B.2 : Less invoiced
                    #     → new_return_picking
                    else:
                        new_return_picking.append(
                            {
                                "product_id": product,
                                "quantity": abs(difference),
                                "sale_line": sale_line,
                                "invoice_line": invoice_line,
                            }
                        )

                # === CASE C : Credit Note
                else:
                    new_return_picking.append(
                        {
                            "product_id": product,
                            "quantity": invoice_line.quantity,
                            "sale_line": sale_line,
                            "invoice_line": invoice_line,
                        }
                    )

            # === 2nd STEP : Create Out Picking
            if new_out_picking:
                self._create_picking_and_move(
                    move,
                    new_out_picking,
                    False,
                )

            # === 3rd STEP : Create Return Picking
            if new_return_picking:
                self._create_picking_and_move(
                    move,
                    new_return_picking,
                    True,
                )
