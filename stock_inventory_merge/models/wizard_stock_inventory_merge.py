# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class WizardStockInventoryMerge(models.TransientModel):
    _name = "wizard.stock.inventory.merge"
    _description = "Stock Inventory Merge Wizard"

    name = fields.Char(string="Inventory Name", required=True)

    @api.multi
    def action_merge(self):
        self.ensure_one()
        inventory_obj = self.env["stock.inventory"]
        context = self.env.context

        # Check valid selection
        if (
            len(context.get("active_ids", [])) < 2
            or context.get("active_model", False) != "stock.inventory"
        ):
            raise UserError(
                _("Please select at least two or more inventories to merge")
            )
        inventories = inventory_obj.browse(context.get("active_ids", []))

        # Check valid state
        if inventories.filtered(lambda x: x.state != "confirm"):
            raise UserError(
                _("Merging is only allowed on 'In Progress' inventories.")
            )

        # Check coherent locations
        locations = inventories.mapped("location_id")
        if len(locations) != 1:
            raise UserError(
                _(
                    "Merging is only allowed on inventories with the same"
                    " location."
                )
            )

        # Create new Inventory and fill with it
        vals = {
            "name": self.name,
            "location_id": locations[0].id,
            "filter": "partial",
            "state": "confirm",
        }
        inventory = inventory_obj.create(vals)
        for line in inventories.mapped("line_ids"):
            line.copy(default={"inventory_id": inventory.id})

        # Return the action focused on the created inventory
        action_data = self.env.ref("stock.action_inventory_form").read()[0]
        action_data["res_id"] = inventory.id
        return action_data
