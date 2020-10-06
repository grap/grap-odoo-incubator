// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.set_inventory", function (require) {
    "use strict";

    var ActionMobileKioskInventory = require("mobile_kiosk_inventory.inventory_action");
    var ajax = require("web.ajax");
    var core = require("web.core");
    var Session = require("web.session");

    var QWeb = core.qweb;

    var ActionSetInventory = ActionMobileKioskInventory.extend({
        template: "MobileAppInventorySetInventory",

        events: {
            "click .button_create_inventory": function() {
                var self = this;
                var inventory_name = this.$('#inventory_name').val().trim();
                if (inventory_name.length === 0) {
                    self.do_warn(
                        _t("Incorrect value"),
                        _t("Please enter a inventory name."),
                        false
                    );
                } else {
                    this._rpc({
                        model: 'mobile.kiosk.inventory',
                        method: 'create_inventory',
                        args: [inventory_name],
                    })
                    .then(function (result) {
                        self.kiosk_notify_result(result);
                        self.kiosk_update_context_from_result(self.kiosk_context, result);

                        // Go to the quantity page
                        self.do_action({
                            type: 'ir.actions.client',
                            name: 'Confirm',
                            tag: "mobile_kiosk_inventory_action_set_product",
                            kiosk_context: self.kiosk_context,
                        });

                    }, function () {
                        self.kiosk_warn_connexion();
                    });
                }
            },


            // "click .button_skip_partner": function() {
            //     // Go to the product page
            //     this.do_action({
            //         type: 'ir.actions.client',
            //         name: 'Select Product',
            //         tag: "mobile_kiosk_inventory_action_set_product",
            //         kiosk_context: this.kiosk_context,
            //     });
            // },
            "click .button_list_inventories": function() {
                this.do_action("mobile_kiosk_inventory.action_stock_inventory_kanban", {
                    additional_context: {
                        "kiosk_action": "mobile_kiosk_inventory_select_inventory",
                        "kiosk_next_tag": "mobile_kiosk_inventory_action_set_product",
                        "kiosk_context": this.kiosk_context,
                        "kiosk_extra_fields": {
                            // "partner_name": "display_name",
                            // "partner_id": "id",
                        },
                    },
                });
            },
        },

    });

    core.action_registry.add("mobile_kiosk_inventory_action_set_inventory", ActionSetInventory);

    return ActionSetInventory;

});
