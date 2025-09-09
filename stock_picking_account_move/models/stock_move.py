# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    # Column Section
    price_unit = fields.Float(
        string="Unit Price (Tax Excluded)",
        digits="Product Price",
        related="product_id.standard_price",
    )

    amount = fields.Float(
        string="Amount (Tax Excluded)",
        store=True,
        compute="_compute_amount",
        digits="Product Price",
    )

    # Compute section
    @api.depends("product_qty", "price_unit", "product_id", "product_uom")
    def _compute_amount(self):
        for line in self:
            if not (line.product_id and line.product_uom):
                continue
            if line.product_uom != line.product_id.uom_id:
                uom_to_use = line.product_id.uom_id
            else:
                uom_to_use = line.product_uom
            # Convert the quantity thanks to new or actual  uom
            line.amount = line.price_unit * line.product_uom._compute_quantity(
                line.product_qty, uom_to_use
            )

    def _get_expense_entry_key_charge(self):
        """
        define how to group by use lines to generate a unique account move
        line for charge move line.
        Overwrite this function to change the behaviour.
        """
        self.ensure_one()
        product = self.product_id
        return (
            product._get_expense_account()["account_expense"].id,
            tuple(product.supplier_taxes_id.ids),
        )

    def _get_expense_entry_key_uncharge(self):
        """
        define how to group by use lines to generate a unique account move
        line for uncharge move line.
        Overwrite this function to change the behaviour.
        """
        self.ensure_one()
        product = self.product_id
        picking_type = self.picking_id.picking_type_id
        return (
            picking_type.account_id.id,
            tuple(product.supplier_taxes_id.ids),
        )

    def _prepare_account_move_line_charge(self, account_move_vals):
        picking_type = self[0].picking_id.picking_type_id
        total = sum(self.mapped("amount"))
        tax_code = self[0].product_id.supplier_taxes_id or False
        return {
            "name": _("Expense Transfert (%s)") % (picking_type.name),
            "product_id": False,
            "product_uom_id": False,
            "quantity": 0,
            "account_id": self[0]
            .product_id._get_expense_account()["account_expense"]
            .id,
            "debit": (total < 0) and -total or 0,
            "credit": (total > 0) and total or 0,
            "tax_ids": tax_code and [(6, 0, [tax_code.id])] or False,
        }

    def _prepare_account_move_line_uncharge(self, account_move_vals):
        picking_type = self[0].picking_id.picking_type_id
        total = sum(self.mapped("amount"))
        tax_code = self[0].product_id.supplier_taxes_id or False
        return {
            "name": _("Expense Transfert (%s)") % (picking_type.name),
            "product_id": False,
            "product_uom_id": False,
            "quantity": 0,
            "account_id": picking_type.account_id.id,
            "debit": (total > 0) and total or 0,
            "credit": (total < 0) and -total or 0,
            "tax_ids": tax_code and [(6, 0, [tax_code.id])] or False,
        }
