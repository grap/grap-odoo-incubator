/*
Copyright (C) 2019-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

openerp.pos_payment_usability = function (instance) {
    'use strict';
    var module = instance.point_of_sale;
    var _t = instance.web._t;

    /** ***********************************************************************
        Extend Model Order:
    */
    var OrderParent = module.Order;
    module.Order = module.Order.extend({

        addPaymentline: function () {
            // Do not add payment line, if the order is empty
            if (this.get('orderLines').length === 0 &&
                    this.get('paymentLines').length === 0) {
                this.pos.pos_widget.screen_selector.show_popup('error', {
                    'message': _t('Empty Order'),
                    'comment': _t('You can not add payment on a empty order '),
                });
                return;
            }

            // If there are an empty payment line, drop it before
            // adding a new one
            if (this.get('paymentLines').length > 0) {
                var paymentLines = this.get('paymentLines').models;
                for (var i = paymentLines.length - 1; i >= 0; i--) {
                    var paymentLine = paymentLines[i];

                    if (paymentLine.amount === 0) {
                        this.removePaymentline(paymentLine);
                    }
                }
            }
            var res = OrderParent.prototype.addPaymentline.apply(
                this, arguments);
            // TODO, check if it is good to keep that feature
            // this.selected_paymentline.node.querySelector('input').value = 0;
            // this.selected_paymentline.set_amount(0);

            return res;
        },

    });

    /** ***********************************************************************
        Extend PaymentScreen Widget:
    */
    module.PaymentScreenWidget = module.PaymentScreenWidget.extend({

        validate_order: function (options) {
            var currentOrder = this.pos.get('selectedOrder');
            var paymentLines = currentOrder.get('paymentLines').models;
            var paidTotal = currentOrder.getPaidTotal();
            var dueTotal = currentOrder.getTotalTaxIncluded();
            var change = paidTotal > dueTotal ? paidTotal - dueTotal : 0;
            if (Math.abs(change) < 0.000001){
                change = 0;
            }
            var cashAmount = 0;

            // Delete payment lines if the amount is null
            for (var i = paymentLines.length - 1; i >= 0; i--) {
                var paymentLine = paymentLines[i];
                if (paymentLine.amount === 0) {
                    currentOrder.removePaymentline(paymentLine);
                }
            }

            // Check if change is over the total amount of cash received
            if (change > 0) {
                for (i = 0; i < paymentLines.length; i++) {
                    paymentLine = paymentLines[i];
                    if (paymentLine.get_type() === 'cash') {
                        cashAmount += paymentLine.amount;
                    }
                }
            }

            // Display a warning if cash amount is under the change
            if (cashAmount < change) {
                this.pos_widget.screen_selector.show_popup('error', {
                    'message': _t('Incorrect Change Value'),
                    'comment': _t(
                        'The change is over the total amount' +
                        ' of cash received'),
                });
                return;
            }

            this._super(options);
        },

        update_payment_summary: function () {
            var currentOrder = this.pos.get('selectedOrder');
            // Var paymentLines = currentOrder.get('paymentLines').models;
            var paidTotal = currentOrder.getPaidTotal();
            var dueTotal = currentOrder.getTotalTaxIncluded();
            var remaining = dueTotal > paidTotal ? dueTotal - paidTotal : 0;

            // Display or hide button to reach the amount
            if (remaining > 0) {
                this.$('.paymentline-set-change button').removeClass(
                    'oe_hidden');
            } else {
                this.$('.paymentline-set-change button').addClass('oe_hidden');
            }

            this._super();
        },

        render_paymentline: function (line) {
            var node = this._super(line);
            node.querySelector('.paymentline-set-change button')
                .addEventListener('click', this.click_set_change);
            return node;
        },

        click_set_change: function (event) {
            var node = this;
            while (node && !node.classList.contains('paymentline')) {
                node = node.parentNode;
            }
            if (node) {
                var currentOrder = node.line.pos.get('selectedOrder');
                var paidTotal = currentOrder.getPaidTotal();
                var dueTotal = currentOrder.getTotalTaxIncluded();
                var remaining = dueTotal > paidTotal ? dueTotal - paidTotal : 0;

                var newAmount = node.line.amount + remaining;
                node.line.set_amount(newAmount);
                node.querySelector('input').value = node.line.get_amount_str();
                currentOrder.selectPaymentline(node.line);

            }
            event.stopPropagation();
        },

    });

    /** ***********************************************************************
        Extend ScreenSelector:
    */
    var ScreenSelectorParent = module.ScreenSelector;
    module.ScreenSelector = module.ScreenSelector.extend({

        // Do not switch to payment screen if the order is empty
        // TODO (PORT V10/12) :: check if it is necessary.
        // this double check (with addPaymentLine) is due to the bad
        // design in Odoo Point of sale in the "click" event of the payment
        // buttons that does'nt allow easy overload
        set_current_screen: function (screen_name) {
            var order = this.pos.get('selectedOrder');
            if (screen_name === 'payment' &&
                    order.get('orderLines').length === 0 &&
                    order.get('paymentLines').length === 0) {
                return;
            }
            return ScreenSelectorParent.prototype.set_current_screen.apply(
                this, arguments);
        },
    });
};
