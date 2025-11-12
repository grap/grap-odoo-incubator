# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class StockMove(models.Model):
    _inherit = "stock.move"

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
        total = sum(self.mapped("total_valuation"))
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
        total = sum(self.mapped("total_valuation"))
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
