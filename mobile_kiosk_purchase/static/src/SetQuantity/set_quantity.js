// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('mobile_kiosk_purchase.set_quantity', function (require) {
    "use strict";

    var ActionMobileKioskPurchase = require("mobile_kiosk_purchase.purchase_action");
    var core = require('web.core');
    var _t = core._t;

    var ActionSetQuantity = ActionMobileKioskPurchase.extend({
        template: "MobileAppPurchaseSetQuantity",

        _mk_has_pad_widget: true,

        _mk_required_fields: [
            "mk_purchase_supplier_id",
            "mk_purchase_supplier_name",
        ],

        events: {
            "click .button_add_quantity": function () {
                var self = this;
                var quantity = parseFloat(this.numpad_widget.get_input_value(), 10);
                this._mk_call_rpc({
                    model: 'mobile.kiosk.purchase',
                    method: "add_quantity",
                    args: [
                        self.mk_context.mk_purchase_supplier_id,
                        self.mk_context.mk_purchase_product_id,
                        quantity,
                    ],
                })
            },
        },

    });

    core.action_registry.add(
        'mobile_kiosk_purchase_action_set_quantity',
        ActionSetQuantity,
    );

    return ActionSetQuantity;

});
