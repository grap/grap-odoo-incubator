// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.set_quantity", function (require) {
    "use strict";

    var ActionMobileKioskInventory = require("mobile_kiosk_inventory.inventory_action");
    var core = require("web.core");
    var _t = core._t;

    var ActionSetQuantity = ActionMobileKioskInventory.extend({
        template: "MobileAppInventorySetQuantity",

        _kiosk_required_fields: [
            "inventory_id",
            "inventory_name",
            "inventory_date",
            "product_id",
            "product_name",
        ],

        _kiosk_pad_widget_required: true,

        events: {
            "click .button_add_quantity": function () {
                var self = this;
                var quantity = parseFloat(this.numpad_widget.get_input_value(), 10);
                if (isNaN(quantity)) {
                    self.do_warn(
                        _t("Incorrect value"),
                        _t("Please enter a valid quantity."),
                        false,
                    );
                } else {
                    this._rpc({
                        model: "mobile.kiosk.inventory",
                        method: "add_quantity",
                        args: [
                            self.kiosk_context.inventory_id,
                            self.kiosk_context.product_id,
                            quantity,
                        ],
                    })
                        .then(function (result) {
                            self.kiosk_notify_result(result);
                            if (result.status === "ok") {
                            // Return to the product page
                                self.do_action({
                                    type: "ir.actions.client",
                                    name: "Select Product",
                                    tag: "mobile_kiosk_inventory_action_set_product",
                                    kiosk_context: self.kiosk_context,
                                });
                            }
                        }, function () {
                            self.kiosk_warn_connexion();
                        });
                }
            },
        },

    });

    core.action_registry.add(
        "mobile_kiosk_inventory_action_set_quantity",
        ActionSetQuantity,
    );

    return ActionSetQuantity;

});
