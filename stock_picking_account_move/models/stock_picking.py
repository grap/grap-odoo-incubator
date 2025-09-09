# Copyright (C) 2025 - Today: GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    _ACCOUNT_MOVE_STATE = [
        ("no_need", "No need"),
        ("waiting", "Waiting"),
        ("to_do", "To Do"),
        ("account_move_generated", "Generated"),
    ]

    # Columns section
    account_move_id = fields.Many2one(
        comodel_name="account.move", string="Account Move", readonly=True, copy=False
    )

    account_move_state = fields.Selection(
        selection=_ACCOUNT_MOVE_STATE,
        string="Account Move Status",
        compute="_compute_account_move_state",
        store=True,
    )

    is_return = fields.Boolean(
        help="Field set True when it's a Picking created by returning one.",
        readonly=True,
    )

    # Compute Section
    @api.depends(
        "state",
        "account_move_id",
        "picking_type_id",
        "picking_type_id.journal_id",
        "picking_type_id.account_id",
    )
    def _compute_account_move_state(self):
        for picking in self:
            if len(picking.picking_type_id.journal_id) != 0:
                if picking.state == "cancel":
                    picking.account_move_state = "no_need"
                elif picking.state == "done":
                    picking.account_move_state = (
                        "account_move_generated" if picking.account_move_id else "to_do"
                    )
                else:
                    picking.account_move_state = "waiting"

            else:
                picking.account_move_state = "no_need"

    def generate_account_move(self):
        """Set the stock pickings to 'done' and create account moves"""
        AccountMove = self.env["account.move"]
        StockMove = self.env["stock.move"]

        picking_data = {}

        # Group pickings by their accounting entry key
        for picking in self.filtered(lambda x: x.account_move_state == "to_do"):
            key = picking._get_expense_entry_key()
            if key in picking_data:
                picking_data[key].append(picking.id)
            else:
                picking_data[key] = [picking.id]

        # Loop through each group of pickings
        for _key, picking_ids in picking_data.items():
            pickings = self.browse(picking_ids)
            account_move_vals = pickings._prepare_account_move()
            all_account_move_line_vals = []

            # Dictionaries to group lines by product, taxes, is_return
            charge_picking_line_data = {}
            uncharge_picking_line_data = {}

            for line in pickings.mapped("move_ids_without_package"):
                charge_line_key = (
                    *line._get_expense_entry_key_charge(),
                    line.picking_id.is_return,
                )
                if charge_line_key in charge_picking_line_data:
                    charge_picking_line_data[charge_line_key].append(line.id)
                else:
                    charge_picking_line_data[charge_line_key] = [line.id]

                uncharge_line_key = (
                    *line._get_expense_entry_key_uncharge(),
                    line.picking_id.is_return,
                )
                if uncharge_line_key in uncharge_picking_line_data:
                    uncharge_picking_line_data[uncharge_line_key].append(line.id)
                else:
                    uncharge_picking_line_data[uncharge_line_key] = [line.id]

            # Generate "uncharge" account move lines
            for (
                _account_id,
                _taxes,
                is_return,
            ), line_ids in uncharge_picking_line_data.items():
                lines = StockMove.browse(line_ids)
                account_move_line_vals = lines._prepare_account_move_line_uncharge(
                    account_move_vals
                )

                # Reverse Debit and Credit if the picking is a return
                if is_return:
                    (
                        account_move_line_vals["debit"],
                        account_move_line_vals["credit"],
                    ) = (
                        account_move_line_vals["credit"],
                        account_move_line_vals["debit"],
                    )

                all_account_move_line_vals.append((0, 0, account_move_line_vals))

            # Generate "charge" account move lines
            for (
                _account_id,
                _taxes,
                is_return,
            ), line_ids in charge_picking_line_data.items():
                lines = StockMove.browse(line_ids)
                account_move_line_vals = lines._prepare_account_move_line_charge(
                    account_move_vals
                )

                # Reverse Debit and Credit if the picking is a return
                if is_return:
                    (
                        account_move_line_vals["debit"],
                        account_move_line_vals["credit"],
                    ) = (
                        account_move_line_vals["credit"],
                        account_move_line_vals["debit"],
                    )

                all_account_move_line_vals.append((0, 0, account_move_line_vals))

            # Create and validate the account move
            account_move_vals["line_ids"] = all_account_move_line_vals
            account_move = AccountMove.create(account_move_vals)
            account_move.action_post()

            # Link pickings to the account move
            pickings.write({"account_move_id": account_move.id})

        return True

    def _get_expense_entry_key(self):
        """
        Define how to group to generare a unique Account Move.
        By default, an entry is generated by Picking_type and by month.
        Overwrite this function to change the behaviour.
        Note that picking_type_id is mandatory.
        """
        self.ensure_one()
        dt = fields.Date.from_string(self.date_done)
        return (
            self.picking_type_id.id,
            "%d-%d" % (dt.year, dt.month),
        )

    def _prepare_account_move(self):
        picking_type = self[0].picking_type_id
        return {
            "journal_id": picking_type.journal_id.id,
            "company_id": picking_type.company_id.id,
            "ref": _("Expense Transfert (%s)") % (picking_type.name),
            "date": max(self.mapped("date_done")),
        }

    def action_mass_generate_wizard(self):
        return {
            "name": _("Mass generate Account Moves"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "stock.picking.mass.generate.wizard",
            "views": [
                [
                    self.env.ref(
                        "stock_picking_account_move.view_stock_picking_mass_generate_wizard_form"
                    ).id,
                    "form",
                ]
            ],
            "target": "new",
        }
