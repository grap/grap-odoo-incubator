// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.set_inventory", function (require) {
    "use strict";

    var ActionMobileKioskInventory = require("mobile_kiosk_inventory.inventory_action");
    var core = require("web.core");

    var ActionSetInventory = ActionMobileKioskInventory.extend({
        template: "MobileAppInventorySetInventory",

        _mk_button_home_page_display: false,

        events: {
            "click .button_create_inventory": function () {
                this._mk_call_rpc({
                    model: "mobile.kiosk.inventory",
                    method: "create_inventory",
                    args: [this.$("#inventory_name").val()],
                });
            },
            "click .button_list_inventories": function () {
                this._mk_do_action("mobile_kiosk_inventory.action_stock_inventory_kanban");
            },
        },

    });

    core.action_registry.add(
        "mobile_kiosk_inventory_action_set_inventory",
        ActionSetInventory,
    );

    return ActionSetInventory;

});
