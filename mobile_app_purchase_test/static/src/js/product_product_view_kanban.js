// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

// TODO : set this view in abstract module

odoo.define('mobile_app_purchase_test.product_product_view_kanban', function(require) {
    "use strict";

    var KanbanRecord = require('web.KanbanRecord');

    KanbanRecord.include({

        _openRecord: function () {
            if (
                    this.modelName === 'product.product'
                    && this.$el.parents('.o_product_product_kanban_kiosk_mode').length
            ) {
                var action = {
                    type: 'ir.actions.client',
                    name: 'Confirm',
                    tag: this.qweb_context.widget.state.context["return_tag"],
                    product_id: this.record.id.raw_value,
                    product_name: this.record.name.raw_value,
                };
                this.do_action(action);
            } else {
                this._super.apply(this, arguments);
            }
        }
    });

});
