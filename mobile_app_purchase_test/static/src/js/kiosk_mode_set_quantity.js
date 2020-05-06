// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('mobile_app_purchase_test.kiosk_mode_set_quantity', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Session = require('web.session');

    var QWeb = core.qweb;

    var KioskModeSetQuantity = AbstractAction.extend({
        template: "MobileAppPurchaseKioskModeSetQuantity",

        events: {
            "click .button_add_quantity": function() {
                var self = this;
                console.log(this);
                var quantity = 40;
                this._rpc({
                    model: 'mobile.app.purchase',
                    method: 'add_quantity',
                    args: [self.product_id, quantity],
                })
                .then(function (result) {
                    console.log("success");
                    // if (result.action) {
                    //     self.do_action(result.action);
                    // } else if (result.warning) {
                    //     self.do_warn(result.warning);
                    //     setTimeout( function() { self.do_action(self.next_action, {clear_breadcrumbs: true}); }, 5000);
                    // }
                }, function () {
                    console.log("error");
                    // setTimeout( function() { self.do_action(self.next_action, {clear_breadcrumbs: true}); }, 5000);
                });


                // Return to the product page
                var action = {
                    type: 'ir.actions.client',
                    name: 'Confirm',
                    tag: "mobile_application_purchase_kiosk_mode_set_product",
                };
                this.do_action(action);
            },
        },

        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.product_id = action.product_id;
            this.product_name = action.product_name;
            console.log(this.getSession());
        },


        start: function () {
            var self = this;

            // Make a RPC call every day to keep the session alive
            self._interval = window.setInterval(this._callServer.bind(this), (60*60*1000*24));
            self.session = Session;

            return this._super.apply(this, arguments);
        },

        renderElement() {
            this._super();
            this.$el.find("#quantity").focus();
        },

        _callServer: function () {
            // Make a call to the database to avoid the auto close of the session
            // TODO, call another keepalive function
            return ajax.rpc("/hr_attendance/kiosk_keepalive", {});
        },

    });

    core.action_registry.add('mobile_application_purchase_kiosk_mode_set_quantity', KioskModeSetQuantity);

    return KioskModeSetQuantity;

});
