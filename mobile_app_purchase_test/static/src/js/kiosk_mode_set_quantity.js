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
        events: {
        },


        start: function () {
            var self = this;

            // Make a RPC call every day to keep the session alive
            self._interval = window.setInterval(this._callServer.bind(this), (60*60*1000*24));
            self.session = Session;

            self.$el.html(QWeb.render("MobileAppPurchaseKioskModeSetQuantity", {widget: self}));

            return this._super.apply(this, arguments);
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
