/*
Copyright (C) 2018-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

"use strict";

openerp.pos_optional_printing = function (instance) {

    var module = instance.point_of_sale;
    var _t = instance.web._t;

    /*************************************************************************
        Extend PaymentScreen Widget:
            * Add a new button Validate 'Without Bill'
    */
    var PaymentScreenWidgetParent = module.PaymentScreenWidget;
    module.PaymentScreenWidget = module.PaymentScreenWidget.extend({
        show: function(){
            this._super();
            var self = this;
            this.add_action_button({
                label: _t('Without Bill'),
                name: 'validation_without_bill',
                icon: '/pos_optional_printing/static/src/img/validate_without_bill.png',
                click: function(){
                    self.validate_order({without_bill: true});
                },
            });
            this.update_payment_summary();
        },

        validate_order: function(options) {
            var currentOrder = this.pos.get('selectedOrder');
            if(options && options.without_bill){
                currentOrder.without_bill = true;
            }
            else{
                currentOrder.without_bill = false;
            }
            if(options && options.invoice){
                // Disable without_bill button if invoiced is selected
                this.pos_widget.action_bar.set_button_disabled('validation_without_bill', true);
            }
            this._super(options);
        },

        update_payment_summary: function() {
            this._super();
            if(this.pos_widget.action_bar){
                this.pos_widget.action_bar.set_button_disabled('validation_without_bill', !this.is_paid());
            }
        },
    });

    /*************************************************************************
        Extend PaymentScreen Widget:
            * Do not call print_receipt with argument if current order
            has been asked to be validated without bill
    */
    var ProxyDeviceParent = module.ProxyDevice;
    module.ProxyDevice = module.ProxyDevice.extend({
        print_receipt: function(receipt, widget){
            if (receipt && this.pos.get('selectedOrder') && this.pos.get('selectedOrder').without_bill){
                return ProxyDeviceParent.prototype.print_receipt.apply(this);
            }
            else {
                return ProxyDeviceParent.prototype.print_receipt.apply(this, arguments);
            }
        },
    });

};
