/*
Copyright (C) 2019-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

"use strict";

openerp.pos_payment_usability = function(instance){

    var module = instance.point_of_sale;
    var _t = instance.web._t;

    /*************************************************************************
        Extend Model Order:
            * 
    */
    var moduleOrderParent = module.Order;
    module.Order = module.Order.extend({

        // Do not add payment line, if the order is empty
        addPaymentline: function(cashregister){
            // Do not add payment line, if the order is empty
            if (this.get('orderLines').length === 0 && this.get('paymentLines').length === 0) {
                this.pos.pos_widget.screen_selector.show_popup('error', {
                    'message': _t('Empty Order'),
                    'comment': _t('You can not add payment on a empty order ')
                });
                return;
            }

            // If there are an empty payment line, drop it before
            // adding a new one
            if (this.get('paymentLines').length > 0){
                var paymentLines = this.get('paymentLines').models;
                for (var i = paymentLines.length - 1; i >=0 ; i--) {
                    var paymentLine = paymentLines[i];

                    if (paymentLine.amount === 0) {
                        // TODO Drop It
                        this.removePaymentline(paymentLine);
                    }
                }
            }
            var res = moduleOrderParent.prototype.addPaymentline.apply(this, arguments);
            // Cancel Odoo Core feature that set by default the total amount
            // for journal that are not 'cash'
            this.selected_paymentline.set_amount(0.0);
            this.selected_paymentline.node.querySelector('.paymentline-input').value = 0;

            return res;
        },

    });

    /*************************************************************************
        Extend Model Order:
            * 
    */
    var modulScreenSelectorParent = module.ScreenSelector;
    module.ScreenSelector = module.ScreenSelector.extend({

        // do not switch to payment screen if the order is empty
        // TODO (PORT V10/12) :: check if it is necessary.
        // this double check (with addPaymentLine) is due to the bad
        // design in Odoo Point of sale in the "click" event of the payment
        // buttons that does'nt allow easy overload
        set_current_screen: function(screen_name, params, refresh){
            var order = this.pos.get('selectedOrder');
            if (screen_name === 'payment' && order.get('orderLines').length === 0 && order.get('paymentLines').length === 0) {
                return;
            }
            return modulScreenSelectorParent.prototype.set_current_screen.apply(this, arguments);
        },
    });


};
