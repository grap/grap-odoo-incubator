// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_abstract.kanban_view_handler", function (require) {
    "use strict";

    var KanbanRecord = require("web.KanbanRecord");

    KanbanRecord.include({

        // Overload this function to create custom hook
        // should return a promise that return a dict that will be added in the returned
        // kiosk_context
        _mobileOpenRecordHook: function () {
            var def = $.Deferred();
            $.when(def).then(function () {
                return {"status": "ok"};
            });
            def.resolve();
            return def;
        },

        _openRecord: function () {
            var self = this;
            if (this.$el.parents(".mobile_kiosk_mode").length) {
                var kiosk_context =
                    this.qweb_context.widget.state.context.kiosk_context || {};
                var fields =
                    this.qweb_context.widget.state.context.kiosk_extra_fields || {};
                Object.keys(fields).forEach(function (key) {
                    kiosk_context[key] = self.record[fields[key]].raw_value;
                });

                this._mobileOpenRecordHook()
                    .then(function (result) {
                        if (result === undefined) {
                            // TODO, fixme don't understand why I don't
                            // receive the result of
                            // the false promise
                            result = {"status": "ok"};
                        }
                        self.kiosk_notify_result(result);
                        if (result.status === "ok") {
                            self.kiosk_update_context_from_result(
                                kiosk_context, result);
                            self.do_action({
                                type: "ir.actions.client",
                                name: "Confirm",
                                tag: self.qweb_context.widget.state.context
                                    .kiosk_next_tag,
                                kiosk_context: kiosk_context,
                            });
                        }
                    }, function () {
                        self.kiosk_warn_connexion();
                    });

            } else {
                this._super.apply(this, arguments);
            }
        },
    });

});
