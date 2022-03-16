// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_purchase.set_supplier", function(require) {
    "use strict";

    var ActionMobileKioskPurchase = require("mobile_kiosk_purchase.purchase_action");
    var core = require("web.core");

    var ActionSetSupplier = ActionMobileKioskPurchase.extend({
        template: "MobileAppPurchaseSetSupplier",

        events: {
            "click .button_skip_partner": function() {
                // Go to the product page
                this.do_action({
                    type: "ir.actions.client",
                    name: "Select Product",
                    tag: "mobile_kiosk_purchase_action_set_product",
                    kiosk_context: this.kiosk_context,
                });
            },
            "click .button_list_partners": function() {
                this.do_action("mobile_kiosk_abstract.action_res_partner_kanban", {
                    additional_context: {
                        kiosk_action: "mobile_kiosk_purchase_select_supplier",
                        kiosk_next_tag: "mobile_kiosk_purchase_action_set_product",
                        kiosk_context: this.kiosk_context,
                        kiosk_extra_fields: {
                            partner_name: "display_name",
                            partner_id: "id",
                        },
                    },
                });
            },
        },
    });

    core.action_registry.add(
        "mobile_kiosk_purchase_action_set_supplier",
        ActionSetSupplier
    );

    return ActionSetSupplier;
});
