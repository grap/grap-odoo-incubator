// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.set_quantity", function (require) {
    "use strict";

    var ActionMobileKioskInventory = require("mobile_kiosk_inventory.inventory_action");
    var core = require("web.core");
    var _t = core._t;

    var ActionSetQuantity = ActionMobileKioskInventory.extend({
        template: "MobileAppInventorySetQuantity",

        _mk_has_pad_widget: true,

        _mk_required_fields: [
            "mk_inventory_inventory_id",
            "mk_inventory_inventory_name",
            "mk_inventory_inventory_date",
            "mk_inventory_product_id",
            "mk_inventory_product_name",
        ],


        events: {
            "click .button_add_quantity": function () {
                var self = this;
                var quantity = parseFloat(this.numpad_widget.get_input_value(), 10);
                this._mk_call_rpc({
                    model: "mobile.kiosk.inventory",
                    method: "add_quantity",
                    args: [
                        self.mk_context.mk_inventory_inventory_id,
                        self.mk_context.mk_inventory_product_id,
                        quantity,
                    ],
                })
            },
        },

    });

    core.action_registry.add("mobile_kiosk_inventory_action_set_quantity", ActionSetQuantity);

    return ActionSetQuantity;

});
