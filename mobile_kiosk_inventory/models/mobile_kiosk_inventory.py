# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class MobileKioskInventory(models.TransientModel):
    _name = "mobile.kiosk.inventory"
    _inherit = "mobile.kiosk.abstract"
    _description = "Mobile Kiosk Inventory Proxy"

    # ################################
    # Public API
    # ################################
    @api.model
    def create_inventory(self, inventory_name):
        result = self._result_prepare()

        # Check inventory_name quality
        inventory_name = inventory_name.strip()
        if not inventory_name:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Missing Inventory Name"),
                message=_("Inventory name is required."),
            )

        # create inventory and start it
        try:
            inventory = self.env["stock.inventory"].create(
                {
                    "name": inventory_name,
                    "filter": "partial",
                }
            )
            inventory.action_start()

        except Exception as _err:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Unable to create inventory"),
                message=str(_err),
            )

        self._result_add_notification(
            result,
            title=_("New Inventory created"),
            message=_("Inventory: %(inventory_name)s", inventory_name=inventory_name),
        )
        result["action"] = self._hook_after_stock_inventory_selection(inventory)
        return result

    @api.model
    def scan_barcode(self, barcode):
        result = self._result_prepare()

        # Search por product
        product = self.env["product.product"].search(
            [("barcode", "=", barcode)], limit=1
        )

        # raise an error if no product was found
        if not product:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Barcode not found"),
                message=_(
                    "No product has been found for barcode '%(barcode)s'.",
                    barcode=barcode,
                ),
            )

        result["action"] = self._hook_after_product_product_selection(product)
        return result

    @api.model
    def add_quantity(self, inventory_id, product_id, product_qty):
        result = self._result_prepare()

        if product_qty is None:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Missing Quantity"),
            )

        if not (isinstance(product_qty, int) or isinstance(product_qty, float)):
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Incorrect Quantity"),
                message=_(
                    "'%(product_qty)s' is not a correct value for a quantity.",
                    product_qty=product_qty,
                ),
            )

        inventory = self.env["stock.inventory"].browse(inventory_id)
        if not inventory:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Inventory not found"),
                message=_(
                    "No inventory has been found for id #%(inventory_id)s.",
                    inventory_id=inventory_id,
                ),
            )
        if inventory.state != "in_progress":
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Inventory in a bad state"),
                message=_(
                    "The inventory %(inventory_name)s is not in a 'In progress' state.",
                    inventory_name=inventory.name,
                ),
            )

        product = self.env["product.product"].browse(product_id)
        if not product:
            return self._result_add_notification(
                result,
                level="danger",
                title=_("Product not found"),
                message=_(
                    "No product has been found for id #%(product_id)s.",
                    product_id=product_id,
                ),
            )

        line = self.env["stock.inventory.line"].search(
            [
                ("inventory_id", "=", inventory_id),
                ("product_id", "=", product_id),
            ],
            limit=1,
        )
        if line:
            old_quantity = line.product_qty
            new_quantity = old_quantity + product_qty
            line.write({"product_qty": new_quantity})
            self._result_add_notification(
                result,
                level="warning",
                title=_("Quantity Changed"),
                message=_(
                    "Product %(product_name)s: quantity inventoried changed from"
                    " %(old_quantity)s to %(new_quantity)s.",
                    product_name=product.name,
                    old_quantity=old_quantity,
                    new_quantity=new_quantity,
                ),
            )
        else:
            line = self.env["stock.inventory.line"].create(
                {
                    "inventory_id": inventory.id,
                    "product_id": product.id,
                    "location_id": inventory.location_id.id,
                    "product_qty": product_qty,
                    "product_uom_id": product.uom_id.id,
                }
            )
            self._result_add_notification(
                result,
                title=_("New Inventory Line"),
                message=_(
                    "The inventory '%(inventory_name)s' has now %(line_qty)s line(s).",
                    inventory_name=inventory.name,
                    line_qty=inventory.line_qty,
                ),
            )

        result["action"] = self._hook_after_quantity_selection(inventory)
        return result

    # ################################
    # Private Function
    # ################################
    @api.model
    def _hook_after_stock_inventory_selection(self, inventory):
        result = {
            "type": "ir.actions.client",
            "name": "Inventory - Select a product",
            "tag": "mobile_kiosk_inventory_action_set_product",
            "target": "fullscreen",
            "context": {
                "mk_inventory_inventory_id": inventory.id,
                "mk_inventory_inventory_name": inventory.name,
                "mk_inventory_inventory_date": inventory.date,
            },
        }
        return result

    @api.model
    def _hook_after_product_product_selection(self, product):
        context = {
            "mk_inventory_product_id": product.id,
            "mk_inventory_product_name": product.name,
        }
        for key in [
            "mk_inventory_inventory_id",
            "mk_inventory_inventory_name",
            "mk_inventory_inventory_date",
        ]:
            context[key] = self.env.context.get(key, False)
        result = {
            "type": "ir.actions.client",
            "name": "Inventory - Put a Quantity",
            "tag": "mobile_kiosk_inventory_action_set_quantity",
            "target": "fullscreen",
            "context": context,
        }
        return result

    @api.model
    def _hook_after_quantity_selection(self, inventory):
        return self._hook_after_stock_inventory_selection(inventory)
