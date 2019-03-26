/*
Copyright (C) 2019-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

"use strict";

openerp.pos_payment_limit = function(instance){

    var module = instance.point_of_sale;
    var _t = instance.web._t;

    /*************************************************************************
        Extend PaymentScreen Widget:
            * Check if payment are over the limit
    */
    module.PaymentScreenWidget = module.PaymentScreenWidget.extend({

        validate_order: function(options) {
            var self = this;
            var currentOrder = this.pos.get('selectedOrder');
            var limit = this.pos.config.payment_limit;
            var paymentLines = currentOrder.get('paymentLines').models;

            for (var i = 0; i < paymentLines.length; i++) {
                var paymentLine = paymentLines[i];
                if (paymentLine.amount > limit) {
                    self.pos_widget.screen_selector.show_popup('error', {
                        'message': _t('Payment Limit Reached'),
                        'comment': _t('The amount of the payment ')
                            + paymentLine.amount + _t(' is over the limit ')
                            + limit,
                    });
                    return;
                }
            }

            this._super(options);
        }
    });

};
