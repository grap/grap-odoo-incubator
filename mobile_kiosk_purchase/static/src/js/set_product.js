// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_purchase.set_product", function (require) {
    "use strict";

    var ActionMobileKioskPurchase = require("mobile_kiosk_purchase.purchase_action");
    var core = require("web.core");

    var ActionSetProduct = ActionMobileKioskPurchase.extend({
        template: "MobileAppPurchaseSetProduct",

        _kiosk_barcode_scanner_required: true,

        // _kiosk_required_fields: [
        //     "partner_id",
        //     "partner_name",
        //     "purchase_order_id",
        //     "purchase_order_name",
        // ],

        events: {
            "click .button_list_products": function () {
                this.do_action("mobile_kiosk_abstract.action_product_product_kanban", {
                    additional_context: {
                        "kiosk_action": "mobile_kiosk_purchase_select_product",
                        "kiosk_next_tag": "mobile_kiosk_purchase_action_set_quantity",
                        "kiosk_error_tag": "mobile_kiosk_purchase_action_set_product",
                        "kiosk_context": this.kiosk_context,
                        "kiosk_extra_fields": {
                            "product_name": "name",
                            "product_id": "id",
                        },
                    },
                });
            },
        },

        _onBarcodeScanned: function (barcode) {
            var self = this;
            this._super.apply(this, arguments);
            this._rpc({
                model: 'mobile.kiosk.purchase',
                method: 'scan_barcode',
                args: [self.kiosk_context.partner_id, barcode],
            })
                .then(function (result) {
                    self.kiosk_notify_result(result);
                    if (result.status === "ok") {
                        self.kiosk_update_context_from_result(
                            self.kiosk_context, result);

                        // Go to the quantity page
                        self.do_action({
                            type: 'ir.actions.client',
                            name: 'Confirm',
                            tag: "mobile_kiosk_purchase_action_set_quantity",
                            kiosk_context: self.kiosk_context,
                        });
                    }
                    self._toggleBarcode(true);
                }, function () {
                    self.kiosk_warn_connexion();
                    self._toggleBarcode(true);
                });

        },
    });

    core.action_registry.add(
        "mobile_kiosk_purchase_action_set_product",
        ActionSetProduct
    );

    return ActionSetProduct;

});
