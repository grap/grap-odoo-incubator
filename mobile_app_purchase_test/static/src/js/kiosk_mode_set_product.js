// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('mobile_app_purchase_test.kiosk_mode_set_product', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Session = require('web.session');

    var QWeb = core.qweb;

    var SylvainWidget = Widget.extend({
        template: "SylvainWidget",

        init:function(parent, options){
            this._super(parent, options);
        },
    });

    var KioskModeSetProduct = AbstractAction.extend({
        template: "MobileAppPurchaseKioskModeSetProduct",


        events: {
            "click .o_product_product_kanban_select_button": function() {
                this.do_action('mobile_app_purchase_test.action_product_product_kanban', {
                    additional_context: {
                        'no_group_by': true,
                        'return_tag': "mobile_application_purchase_kiosk_mode_set_quantity",
                    },
                });
            },
        },

        start: function () {
            console.log("KioskModeSetProduct::start");
            var self = this;
            core.bus.on('barcode_scanned', this, this._onBarcodeScanned);

            // Make a RPC call every day to keep the session alive
            self._interval = window.setInterval(this._callServer.bind(this), (60*60*1000*24));
            self.session = Session;


            // console.log($(".placeholder-SylvainWidget"));
            // console.log(this.$el);
            // console.log(this.$el.find(".placeholder-SylvainWidget"));
            // console.log("================");
            return this._super.apply(this, arguments);
        },

        renderElement: function () {
            this._super();
            var mySylvainWidget = new SylvainWidget(this, {});
            // mySylvainWidget.appendTo(this.$el.find(".placeholder-SylvainWidget"));
            console.log("================");
            console.log(this.$(".placeholder-SylvainWidget"));
            console.log(this.$el.find(".placeholder-SylvainWidget"));
            console.log("================");
            mySylvainWidget.appendTo(this.$(".placeholder-SylvainWidget"));
        },

        _onBarcodeScanned: function(barcode) {
            var self = this;
            core.bus.off('barcode_scanned', this, this._onBarcodeScanned);
            console.log("_onBarcodeScanned");
        },


        destroy: function () {
            core.bus.off('barcode_scanned', this, this._onBarcodeScanned);
            clearInterval(this._interval);
            this._super.apply(this, arguments);
        },

        _callServer: function () {
            // Make a call to the database to avoid the auto close of the session
            // TODO, call another keepalive function
            return ajax.rpc("/hr_attendance/kiosk_keepalive", {});
        },

    });

    core.action_registry.add('mobile_application_purchase_kiosk_mode_set_product', KioskModeSetProduct);

    return KioskModeSetProduct;

});