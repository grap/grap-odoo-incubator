// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_abstract.abstract_action", function(require) {
    "use strict";

    var AbstractAction = require("web.AbstractAction");
    var PadWidget = require("mobile_kiosk_abstract.pad_widget");
    var ajax = require("web.ajax");
    var core = require("web.core");
    var session = require("web.session");

    var ActionMobileKioskAbstract = AbstractAction.extend({
        // Set to True if you want enable the call of the function
        // _onBarcodeScanned, when a barcode is scanned
        _kiosk_barcode_scanner_required: false,

        // Set to True if you want to display a padwidget in your kiosk screen
        // note: you should have a >div class="placeholder-padwidget" />
        // in your screen.
        _kiosk_pad_widget_required: false,

        // At the start() of the action, we'll check if there fields are
        // present in the context. If not, we go back the home page
        _kiosk_required_fields: [],

        _kiosk_home_page_tag: false,
        _kiosk_home_page_name: false,

        _kiosk_abstract_events: {
            "click .button_home_page": function() {
                this.do_action({
                    type: "ir.actions.client",
                    name: this._kiosk_home_page_name,
                    tag: this._kiosk_home_page_tag,
                });
            },
        },

        init: function(parent, action) {
            var self = this;

            // Add events that will be raised for each action that
            // inherit of this abstract action
            Object.keys(this._kiosk_abstract_events).forEach(function(event_key) {
                self.events[event_key] = self._kiosk_abstract_events[event_key];
            });

            // Recover context
            this.kiosk_context = action.kiosk_context || {};

            // Check if the context if valid. If not, the interface will propose
            // to go to the home page
            this.kiosk_should_go_back = false;
            this._kiosk_required_fields.forEach(function(required_key) {
                if (self.kiosk_context[required_key] === undefined) {
                    self.kiosk_should_go_back = true;
                }
            });
            this._super.apply(this, arguments);
        },

        renderElement: function() {
            this._super();
            // Create and render a PadWidget if required
            if (this._kiosk_pad_widget_required) {
                this.numpad_widget = new PadWidget(this, {});
                this.numpad_widget.appendTo(this.$(".placeholder-padwidget"));
            }
        },

        start: function() {
            this.session = session;

            // Make a RPC call every day to keep the session alive
            this._interval = window.setInterval(
                this._callServer.bind(this),
                60 * 60 * 1000 * 24
            );

            // Enable barcode if required
            this._toggleBarcode(true);

            return this._super.apply(this, arguments);
        },

        destroy: function() {
            // Disable RPC call to keep session alive
            clearInterval(this._interval);
            // Disable barcode if it has been enabled
            this._toggleBarcode(false);
            this._super.apply(this, arguments);
        },

        _toggleBarcode: function(active) {
            if (this._kiosk_barcode_scanner_required) {
                if (active) {
                    core.bus.on("barcode_scanned", this, this._onBarcodeScanned);
                } else {
                    core.bus.off("barcode_scanned", this, this._onBarcodeScanned);
                }
            }
        },

        _onBarcodeScanned: function() {
            this._toggleBarcode(false);
        },

        _callServer: function() {
            // Make a call to the database to avoid the auto close of the session
            return ajax.rpc("/mobile_kiosk_abstract/kiosk_keepalive", {});
        },
    });

    return ActionMobileKioskAbstract;
});
