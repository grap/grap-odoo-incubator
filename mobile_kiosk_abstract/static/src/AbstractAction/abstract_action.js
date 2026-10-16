// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('mobile_kiosk_abstract.abstract_action', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var PadWidget = require('mobile_kiosk_abstract.pad_widget');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var session = require('web.session');
    var _t = core._t;


    var ActionMobileKioskAbstract = AbstractAction.extend({

        // Set to True if you want enable the call of the function
        // _mk_onBarcodeScanned, when a barcode is scanned
        _mk_has_barcode_scanner: false,

        // Set to True if you want to display a padwidget in your kiosk screen
        // note: you should have a >div class="placeholder-padwidget" />
        // in your screen.
        _mk_has_pad_widget: false,

        // At the start() of the action, we'll check if there fields are
        // present in the context. If not, we go back the home page
        _mk_required_fields: [],

        _mk_home_page_tag: false,
        _mk_button_home_page_display: true,

        _mk_events: {
            "click .button_home_page": function () {
                this.do_action({
                    type: 'ir.actions.client',
                    name: this._mk_title,
                    tag: this._mk_home_page_tag,
                    target: "fullscreen",
                });
            },
            "click .button_exit": function () {
                window.location = "/web#action=";
            },
        },

        _mk_title: function () {
            return _t("Application");
        },

        _mk_call_rpc: function (params) {
            var self = this;

            return this._rpc(params).then(function (result) {
                // 1. display notification(s), if any
                var notifications = result.notifications || [];
                notifications.forEach(function (notification) {
                        self.displayNotification(notification);
                });

                // 2. Go to next action, if defined
                if (result.action) {
                    self.do_action(result["action"]);
                }
            }, function () {
                self.displayNotification({
                    title: _t("Connexion lost"),
                    message: _t("Please check your Internet Connexion, then try again"),
                    type: "danger",
                });
            });
        },

        _mk_do_action: function (action_name) {
            var context = this.mk_context;
            this.do_action(action_name, {clear_breadcrumbs: true, additional_context: context});
        },

        _mk_toggleBarcode: function (active) {
            if (this._mk_has_barcode_scanner) {
                if (active) {
                    core.bus.on('barcode_scanned', this, this._mk_onBarcodeScanned);
                } else {
                    core.bus.off('barcode_scanned', this, this._mk_onBarcodeScanned);
                }
            }
        },

        _mk_onBarcodeScanned: function () {
            this._mk_toggleBarcode(false);
        },

        _mk_callServer: function () {
            // Make a call to the database to avoid the auto close of the session
            return ajax.rpc("/mobile_kiosk_abstract/kiosk_keepalive", {});
        },

        init: function (parent, action) {
            var self = this;

            // Add events that will be raised for each action that
            // inherit of this abstract action
            Object.keys(this._mk_events).forEach(function (event_key) {
                self.events[event_key] = self._mk_events[event_key];
            });

            // Recover and store context of the original action
            this.mk_context = action.context || {};

            // Check if the context if valid. If not, the interface will propose
            // to go to the home page
            this.mk_should_go_back = false;
            this._mk_required_fields.forEach(function (required_key) {
                if (!self.mk_context[required_key]) {
                    self.mk_should_go_back = true;
                }
            });

            this._super.apply(this, arguments);
        },

        renderElement: function () {
            this._super();
            // Create and render a PadWidget if required
            if (this._mk_has_pad_widget) {
                this.numpad_widget = new PadWidget(this, {});
                this.numpad_widget.appendTo(this.$('.placeholder-padwidget'));
            }
        },

        start: function () {
            this.session = session;

            // Make a RPC call every day to keep the session alive
            this._interval = window.setInterval(
                this._mk_callServer.bind(this), 60*60*1000*24);

            // Enable barcode if required
            this._mk_toggleBarcode(true);

            return this._super.apply(this, arguments);
        },

        destroy: function () {
            // Disable RPC call to keep session alive
            clearInterval(this._interval);
            // Disable barcode if it has been enabled
            this._mk_toggleBarcode(false);
            this._super.apply(this, arguments);
        },

    });

    return ActionMobileKioskAbstract;

});
