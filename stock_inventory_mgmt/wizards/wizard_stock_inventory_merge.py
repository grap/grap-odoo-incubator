# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, fields, models
from odoo.exceptions import UserError


class WizardStockInventoryMerge(models.TransientModel):
    _name = "wizard.stock.inventory.merge"
    _description = "Stock Inventory Merge Wizard"

    name = fields.Char(
        string="Inventory Name", required=True, default=lambda x: x._default_name()
    )

    def _default_name(self):
        lang = self.env["res.lang"].search(
            [("code", "=", self.env.user.lang or "en_US")]
        )
        date_format = lang and lang.date_format or "%m/%d/%Y"
        return _(
            "Complete Inventory of %(date_string)s",
            date_string=fields.Datetime.now().strftime(date_format),
        )

    def action_merge(self):
        self.ensure_one()
        StockInventory = self.env["stock.inventory"]
        context = self.env.context

        # Check valid selection
        inventories = StockInventory.browse(context.get("active_ids", []))
        if len(inventories) < 2:
            raise UserError(
                _("Please select at least two or more inventories to merge")
            )

        # Check negative lines
        negative_lines = inventories.mapped("line_ids").filtered(
            lambda x: x.product_qty < 0
        )
        if negative_lines:
            raise UserError(
                _(
                    "Merging is only allowed on inventories"
                    " that doesn't contains negative values.\n\n- %(inventory_names)s",
                    inventory_names="\n- ".join(
                        negative_lines.mapped("inventory_id.name")
                    ),
                )
            )

        # Check valid state
        if inventories.filtered(lambda x: x.state != "in_progress"):
            raise UserError(_("Merging is only allowed on 'In Progress' inventories."))

        # Check valid type (filter)
        if inventories.filtered(lambda x: x.filter == "none"):
            raise UserError(_("Merging is not allowed for Full inventories."))

        # Check coherent locations
        if len(inventories.mapped("location_id")) > 1:
            raise UserError(
                _("Merging is only allowed on inventories with the same location.")
            )

        # Create new Inventory and fill with it
        new_inventory = StockInventory.create(
            {
                "name": self.name,
                "location_id": inventories[0].location_id.id,
                "filter": "none",
                "exhausted": True,
            }
        )
        new_inventory.action_start()

        # Populate a dictionary of all the empty lines
        lines_dict = {}
        for line in new_inventory.mapped("line_ids"):
            lines_dict[line._get_keys()] = line

        # compute
        for line in inventories.mapped("line_ids").filtered(
            lambda x: x.product_qty != 0
        ):
            key = line._get_keys()
            if key in lines_dict:
                lines_dict[key].product_qty += line.product_qty
            else:
                new_line = line.copy({"inventory_id": new_inventory.id})
                lines_dict[key] = new_line

            line.merged_inventory_line_id = lines_dict[key].id

        inventories.write({"merged_inventory_id": new_inventory.id})
        inventories.write({"state": "pending_merge"})

        # Return the action focused on the created inventory
        action_data = self.env.ref("stock_inventory_mgmt.action_inventory_form").read()[
            0
        ]
        view = self.env.ref("stock_inventory_mgmt.view_inventory_form")
        action_data["views"] = [(view.id, "form")]
        action_data["res_id"] = new_inventory.id
        return action_data
