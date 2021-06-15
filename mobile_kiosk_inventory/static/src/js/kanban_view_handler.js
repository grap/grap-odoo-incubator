// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.kanban_view_handler", function (require) {
    "use strict";

    var KanbanRecord = require("web.KanbanRecord");

    KanbanRecord.include({
        // When selecting an inventory, we will load it
        _mobileOpenRecordHook: function () {
            var self = this;
            var context = this.qweb_context.widget.state.context;
            if (context.kiosk_action === undefined) {
                return this._super.apply(this, arguments);
            }
            if (context.kiosk_action === "mobile_kiosk_inventory_select_inventory") {
                return self
                    ._rpc({
                        model: "mobile.kiosk.inventory",
                        method: "select_inventory",
                        args: [self.recordData.id],
                    })
                    .then(function (result) {
                        return result;
                    });
            } else if (
                context.kiosk_action === "mobile_kiosk_inventory_select_product"
            ) {
                return self
                    ._rpc({
                        model: "mobile.kiosk.inventory",
                        method: "select_product",
                        args: [
                            context.kiosk_context.inventory_id,
                            self.record.id.raw_value,
                        ],
                    })
                    .then(function (result) {
                        return result;
                    });
            }
            return this._super.apply(this, arguments);
        },
    });
});
