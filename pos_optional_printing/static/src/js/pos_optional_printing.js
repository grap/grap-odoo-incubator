/*
Copyright (C) 2018-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

"use strict";

console.log("IN JS FILE");

openerp.pos_optional_printing = function (instance) {

    var module = instance.point_of_sale;
    var _t = instance.web._t;

    console.log("MODULE LOADED");

    /*************************************************************************
        Extend PaymentScreen Widget:
            * Add a new button Validate 'Without Bill'
    */
    var PaymentScreenWidgetParent = module.PaymentScreenWidget;
    module.PaymentScreenWidget = module.PaymentScreenWidget.extend({
        show: function(){
            console.log("show::overloaded");
            this._super();
            var self = this;
            this.add_action_button({
                label: _t('Without Bill'),
                name: 'validation_without_bill',
                icon: '/point_of_sale/static/src/img/icons/png48/validate.png',
                click: function(){
                    self.validate_order({without_bill: true});
                },
            });
        },

        validate_order: function(options) {
            console.log("validate_order::overloaded");
            var currentOrder = this.pos.get('selectedOrder');
            if(options.without_bill){
                currentOrder.without_bill = true;
            }
            else{
                currentOrder.without_bill = false;
            }
            if(options.invoice){
                // Disable without_bill button if invoiced is selected
                this.pos_widget.action_bar.set_button_disabled('validation_without_bill',true);
            }
            this._super(options);
        },

        update_payment_summary: function() {
            console.log("update_payment_summary::overloaded");
            this._super();
            if(this.pos_widget.action_bar){
                this.pos_widget.action_bar.set_button_disabled('validation_without_bill', !this.is_paid());
            }
        },


    });


    /*************************************************************************
        Extend Model Order:
            * Return result of export_for_printing only if asked by the user
    */
    var moduleOrderParent = module.Order;
    module.Order = module.Order.extend({

        export_for_printing: function(attributes){
            console.log("export_for_printing::overloaded");
            var res = moduleOrderParent.prototype.export_for_printing.apply(this, arguments);
            if (this.without_bill){
                return false;
            }
            else{
                return res;
            }
        },

    });



//    /* 
//        Define : New ErrorClosedSessionPopupWidget Widget.
//        This pop up will be shown if the current pos.session of the PoS is not
//        in an 'open' state;
//        The check will be done depending on a parameter on the PoS config
//    */  
//    module.ErrorClosedSessionPopupWidget = module.ErrorPopupWidget.extend({
//        template:'ErrorClosedSessionPopupWidget',

//        session_name: '',

//        init: function(parent, options) {
//            var self = this;
//            this._super(parent, options);

//            self.intervalID = setInterval(function() {
//                self.pos.fetch('pos.session', ['name','state'], [['id', '=', self.pos.pos_session.id]]) 
//                .then(function(sessions){
//                    if (sessions[0]['state'] != 'opened') {
//                        // warn user if current session is not opened
//                        self.session_name = sessions[0]['name'];
//                        self.renderElement();
//                        self.pos_widget.screen_selector.show_popup('error-closed-session');
//                        clearInterval(self.intervalID);
//                    }
//                })
//                .fail(function(error, event){
//                    // Prevent error if server is unreachable
//                    event.preventDefault();
//                });
//            }, self.pos.config.check_session_state_frequency * 1000);
//        },
//    });

//    /* 
//        Overload : PosWidget to include ErrorClosedSessionPopupWidget inside.
//    */
//    module.PosWidget = module.PosWidget.extend({
//        build_widgets: function(){
//            this._super();
//            // Add a new Popup 'ErrorClosedSessionPopupWidget'
//            this.error_closed_session_popup = new module.ErrorClosedSessionPopupWidget(this, {});
//            this.error_closed_session_popup.appendTo(this.$el);
//            this.screen_selector.popup_set['error-closed-session'] = this.error_closed_session_popup;

//            // Hide the popup because all pop up are displayed at the
//            // beginning by default
//            this.error_closed_session_popup.hide();
//        },
//    });

};
