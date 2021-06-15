// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.set_product", function (require) {
    "use strict";

    var ActionMobileKioskInventory = require("mobile_kiosk_inventory.inventory_action");
    var core = require("web.core");

    var ActionSetProduct = ActionMobileKioskInventory.extend({
        template: "MobileAppInventorySetProduct",

        _kiosk_barcode_scanner_required: true,

        _kiosk_required_fields: ["inventory_id", "inventory_name", "inventory_date"],

        events: {
            "click .button_list_products": function () {
                this.do_action("mobile_kiosk_abstract.action_product_product_kanban", {
                    additional_context: {
                        kiosk_action: "mobile_kiosk_inventory_select_product",
                        kiosk_next_tag: "mobile_kiosk_inventory_action_set_quantity",
                        kiosk_error_tag: "mobile_kiosk_inventory_action_set_product",
                        kiosk_context: this.kiosk_context,
                        kiosk_extra_fields: {
                            product_name: "name",
                            product_id: "id",
                        },
                    },
                });
            },
        },

        _onBarcodeScanned: function (barcode) {
            var self = this;
            this._super.apply(this, arguments);
            this._rpc({
                model: "mobile.kiosk.inventory",
                method: "scan_barcode",
                args: [self.kiosk_context.inventory_id, barcode],
            }).then(
                function (result) {
                    self.kiosk_notify_result(result);
                    if (result.status === "ok") {
                        self.kiosk_update_context_from_result(
                            self.kiosk_context,
                            result
                        );

                        // Go to the quantity page
                        self.do_action({
                            type: "ir.actions.client",
                            name: "Confirm",
                            tag: "mobile_kiosk_inventory_action_set_quantity",
                            kiosk_context: self.kiosk_context,
                        });
                    }
                    self._toggleBarcode(true);
                },
                function () {
                    self.kiosk_warn_connexion();
                    self._toggleBarcode(true);
                }
            );
        },
    });

    core.action_registry.add(
        "mobile_kiosk_inventory_action_set_product",
        ActionSetProduct
    );

    return ActionSetProduct;
});
