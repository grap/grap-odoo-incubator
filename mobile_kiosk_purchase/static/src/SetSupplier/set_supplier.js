// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_purchase.set_supplier", function (require) {
    "use strict";

    var ActionMobileKioskPurchase = require("mobile_kiosk_purchase.purchase_action");
    var core = require("web.core");

    var ActionSetSupplier = ActionMobileKioskPurchase.extend({
        template: "MobileAppPurchaseSetSupplier",

        _mk_button_home_page_display: false,

        _mk_required_fields: [],

        events: {
            "click .button_list_partners": function () {
                this._mk_do_action("mobile_kiosk_purchase.action_res_partner_kanban");
            },
        },

    });

    core.action_registry.add(
        "mobile_kiosk_purchase_action_set_supplier",
        ActionSetSupplier,
    );

    return ActionSetSupplier;

});
