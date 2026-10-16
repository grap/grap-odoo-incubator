// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.set_product", function (require) {
    "use strict";

    var ActionMobileKioskInventory = require("mobile_kiosk_inventory.inventory_action");
    var core = require("web.core");

    var ActionSetProduct = ActionMobileKioskInventory.extend({
        template: "MobileAppInventorySetProduct",

        _mk_has_barcode_scanner: true,

        _mk_required_fields: [
            "mk_inventory_inventory_id",
            "mk_inventory_inventory_name",
            "mk_inventory_inventory_date",
        ],

        events: {
            "click .button_list_products": function () {
                this._mk_do_action("mobile_kiosk_inventory.action_product_product_kanban");
            },
        },

        _mk_onBarcodeScanned: function (barcode) {
            var self = this;
            this._super.apply(this, arguments);
            this._mk_call_rpc({
                model: "mobile.kiosk.inventory",
                method: "scan_barcode",
                args: [barcode],
            }).then( function (){
                self._mk_toggleBarcode(true);
            });
        },

    });

    core.action_registry.add("mobile_kiosk_inventory_action_set_product", ActionSetProduct);

    return ActionSetProduct;

});
