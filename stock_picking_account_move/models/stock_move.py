# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_expense_entry_key(self):
        """
        Define how to group by use lines to generate a unique account move
        line for many stock moves.
        """
        self.ensure_one()
        return (
            self.product_id._get_product_accounts()["expense"],
            tuple(self.product_id.supplier_taxes_id),
        )

    def _prepare_account_move_line_charge(
        self, stock_picking_entry_key, stock_move_entry_key, account_move_vals
    ):
        total = sum(self.mapped("total_valuation"))
        if stock_picking_entry_key[1] == "opposite":
            total -= total
        account = stock_move_entry_key[0]
        taxes = stock_move_entry_key[1]
        return {
            "name": account_move_vals["ref"],
            "product_id": False,
            "product_uom_id": False,
            "quantity": 0,
            "account_id": account.id,
            "debit": (total < 0) and -total or 0,
            "credit": (total > 0) and total or 0,
            "tax_ids": taxes and [(6, 0, [tax.id for tax in taxes])] or False,
        }

    def _prepare_account_move_line_uncharge(
        self, stock_picking_entry_key, stock_move_entry_key, account_move_vals
    ):
        picking_type = stock_picking_entry_key[0]
        total = sum(self.mapped("total_valuation"))
        if stock_picking_entry_key[1] == "opposite":
            total -= total
        taxes = stock_move_entry_key[1]
        return {
            "name": account_move_vals["ref"],
            "product_id": False,
            "product_uom_id": False,
            "quantity": 0,
            "account_id": picking_type.account_id.id,
            "debit": (total > 0) and total or 0,
            "credit": (total < 0) and -total or 0,
            "tax_ids": taxes and [(6, 0, [tax.id for tax in taxes])] or False,
        }
