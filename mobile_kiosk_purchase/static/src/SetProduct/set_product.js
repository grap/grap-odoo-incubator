// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_purchase.set_product", function (require) {
    "use strict";

    var ActionMobileKioskPurchase = require("mobile_kiosk_purchase.purchase_action");
    var core = require("web.core");

    var ActionSetProduct = ActionMobileKioskPurchase.extend({
        template: "MobileAppPurchaseSetProduct",

        _mk_has_barcode_scanner: true,

        _mk_required_fields: [
            "mk_purchase_supplier_id",
            "mk_purchase_supplier_name",
        ],

        events: {
            "click .button_list_products": function () {
                this._mk_do_action("mobile_kiosk_purchase.action_product_product_kanban");
            },
        },

        _mk_onBarcodeScanned: function (barcode) {
            var self = this;
            this._super.apply(this, arguments);
            this._mk_call_rpc({
                model: "mobile.kiosk.purchase",
                method: "scan_barcode",
                args: [barcode, self.mk_context.mk_purchase_supplier_id],
            }).then( function (){
                self._mk_toggleBarcode(true);
            });
        },

    });

    core.action_registry.add(
        "mobile_kiosk_purchase_action_set_product",
        ActionSetProduct,
    );

    return ActionSetProduct;

});
