# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class StockInventory(models.Model):
    _inherit = "stock.inventory"
    _order = "date desc"

    filter = fields.Selection(default="partial")

    duplicates_qty = fields.Integer(
        string="Duplicates Quantity", compute="_compute_duplicates_qty"
    )

    _INVENTORY_LINE_KEY_FIELDS = [
        "product_id",
        "location_id",
        "partner_id",
        "package_id",
        "prod_lot_id",
    ]

    # Compute Section
    @api.multi
    def _compute_duplicates_qty(self):
        for inventory in self:
            inventory.duplicates_qty = len(inventory._get_duplicated_line_ids())

    # Overload Section
    @api.multi
    def action_validate(self):
        inventories = self.filtered(lambda x: x.duplicates_qty)
        if inventories:
            raise UserError(
                _(
                    "You can not confirm '%s' because there are"
                    " some duplicated lines."
                    % (", ".join([x.name for x in inventories]))
                )
            )
        return super(StockInventory, self).action_validate()

    # Action Section
    @api.multi
    def action_view_duplicates(self):
        self.ensure_one()
        action = self.env.ref("stock_inventory_merge.action_view_duplicates_tree")
        action_data = action.read()[0]
        duplicates_list = self._get_duplicated_line_ids()
        duplicate_ids = []
        for duplicates in duplicates_list:
            duplicate_ids += duplicates
        action_data["domain"] = (
            "[('id','in',[" + ",".join(map(str, duplicate_ids)) + "])]"
        )
        return action_data

    @api.multi
    def complete_with_zero(self):
        line_obj = self.env["stock.inventory.line"]
        for inventory in self:
            product_lines = inventory._get_inventory_lines_values()
            current_vals = inventory._get_inventory_line_vals()
            for product_line in product_lines:
                # Check if the line is in the inventory
                found = False
                for item in current_vals:
                    if self._get_inventory_line_keys(
                        item
                    ) == self._get_inventory_line_keys(product_line):
                        found = True
                        break
                if not found:
                    # Add the line, if inventory line was not found
                    product_line["product_qty"] = 0
                    product_line["inventory_id"] = self.id
                    line_obj.create(product_line)

    @api.multi
    def action_merge_duplicated_line(self):
        uom_obj = self.env["uom.uom"]
        line_obj = self.env["stock.inventory.line"]
        for inventory in self:
            line_group_ids = inventory._get_duplicated_line_ids()
            for line_ids in line_group_ids:
                sum_quantity = 0
                keeped_line_id = False
                default_uom_id = False
                for line_data in line_obj.search_read(
                    [("id", "in", line_ids)], ["product_uom_id", "product_qty"]
                ):
                    if not keeped_line_id:
                        keeped_line_id = line_data["id"]
                        default_uom_id = line_data["product_uom_id"][0]
                        sum_quantity = line_data["product_qty"]
                    else:
                        # Same UoM
                        if default_uom_id == line_data["product_uom_id"][0]:
                            sum_quantity += line_data["product_qty"]
                        else:
                            uom_id = line_data["product_uom_id"][0]
                            sum_quantity += uom_obj.browse(uom_id)._compute_quantity(
                                line_data["product_qty"],
                                uom_obj.browse(default_uom_id),
                            )

                # Update the first line with the sumed quantity
                keeped_line = line_obj.browse(keeped_line_id)
                keeped_line.write({"product_qty": sum_quantity})

                # Delete all the other lines
                line_ids.remove(keeped_line_id)
                line_obj.browse(line_ids).unlink()

    # Custom Section
    @api.multi
    def _get_duplicated_line_ids(self):
        self.ensure_one()
        check_dict = {}
        duplicates_group_ids = []
        line_vals = self._get_inventory_line_vals()
        for line_val in line_vals:
            key = self._get_inventory_line_keys(line_val)
            if key in check_dict:
                check_dict[key].append(line_val["id"])
            else:
                check_dict[key] = [line_val["id"]]
        for _k, v in check_dict.items():
            if len(v) > 1:
                duplicates_group_ids.append(v)
        return duplicates_group_ids

    @api.multi
    def _get_inventory_line_vals(self):
        line_obj = self.env["stock.inventory.line"]
        return line_obj.search_read(
            [("inventory_id", "in", self.ids)], self._INVENTORY_LINE_KEY_FIELDS
        )

    @api.model
    def _get_inventory_line_keys(self, values):
        res = []
        for field in self._INVENTORY_LINE_KEY_FIELDS:
            if values.get(field, False):
                if type(values.get(field)) is tuple:
                    res.append(values.get(field)[0])
                else:
                    res.append(values.get(field))
            else:
                res.append(False)
        return str(res)
