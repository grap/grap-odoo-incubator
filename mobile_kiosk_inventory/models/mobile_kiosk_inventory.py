# Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class MobileKioskInventory(models.TransientModel):
    _name = "mobile.kiosk.inventory"
    _inherit = "mobile.kiosk.abstract"
    _description = "Mobile Kiosk Inventory Proxy"

    @api.model
    def create_inventory(self, inventory_name):
        result = self._prepare_result()

        StockInventory = self.env["stock.inventory"]
        StockLocation = self.env["stock.location"]
        locations = StockLocation.search([("usage", "=", "internal")])
        if len(locations) == 0:
            return self._add_result_error(
                result,
                "Locations not found",
                _("No internal locations has been found."),
            )

        inventory = StockInventory.create({
            "name": inventory_name,
            "filter": "partial",
            "location_id": locations[0].id,
        })
        inventory.action_start()

        self._prepare_stock_inventory_data(result, inventory)

        return result

    @api.model
    def select_inventory(self, inventory_id):
        """Select the inventory"""
        result = self._prepare_result()

        # Get an inventory, or raise an error
        self._select_stock_inventory(inventory_id, result)

        return result

    @api.model
    def select_product(self, inventory_id, product_id):
        result = self._prepare_result()

        self._select_product(inventory_id, product_id, result)
        return result

    @api.model
    def scan_barcode(self, partner_id, barcode):
        result = self._prepare_result()
        ProductProduct = self.env["product.product"]

        # Get product or raise an error
        products = ProductProduct.search([("barcode", "=", barcode)])
        if not products:
            return self._add_result_error(
                result,
                "Barcode not found",
                _("No product has been found for barcode '%s'" % barcode),
            )
        self._select_product(partner_id, products[0].id, result)
        return result

    @api.model
    def add_quantity(self, inventory_id, product_id, product_qty):
        result = self._prepare_result()
        ProductProduct = self.env["product.product"]
        StockInventory = self.env["stock.inventory"]
        StockInventoryLine = self.env["stock.inventory.line"]

        inventory = StockInventory.browse(inventory_id)
        product = ProductProduct.browse(product_id)

        lines = StockInventoryLine.search([
            ('inventory_id', '=', inventory_id),
            ('product_id', '=', product_id),
        ])
        if lines:
            line = lines[0]
            old_quantity = line.product_qty
            new_quantity = old_quantity + product_qty
            lines[0].write({'product_qty': new_quantity})
            self._add_result_notify(
                result,
                _("Quantity Changed"),
                _("Quantity inventoried changed from %s to %s" % (
                    old_quantity, new_quantity))
            )
        else:
            line = StockInventoryLine.create({
                "inventory_id": inventory.id,
                "product_id": product.id,
                "location_id": inventory.location_id.id,
                "product_qty": product_qty,
                "product_uom_id": product.uom_id.id,
            })
        return result

    @api.model
    def _select_stock_inventory(self, inventory_id, result):
        StockInventory = self.env["stock.inventory"]

        inventories = StockInventory.search([
            ("id", "=", inventory_id),
            ("state", "in", self._get_stock_inventory_loadable_state())
        ])
        if not inventories:
            self._add_result_error(
                result,
                "Inventory not found",
                _("The selected inventory has been dropped, or confirmed.")
            )
            return

        else:
            inventory = inventories[0]
        self._prepare_stock_inventory_data(result, inventory)

    def _select_product(self, inventory_id, product_id, result):
        ProductProduct = self.env["product.product"]

        products = ProductProduct.search([
            ("id", "=", product_id),
        ])
        if not products:
            self._add_result_error(
                result,
                "Product not found",
                _("The product has been dropped, or disabled.")
            )
            return

        else:
            product = products[0]

        self._prepare_product_data(result, product)

    @api.model
    def _prepare_stock_inventory_data(self, result, stock_inventory):
        result.update({
            "inventory_id": stock_inventory.id,
            "inventory_name": stock_inventory.name,
            "inventory_date": stock_inventory.date,
        })

    @api.model
    def _get_stock_inventory_loadable_state(self):
        return ["confirm"]
