/******************************************************************************
    Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
    @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 *****************************************************************************/

"use strict";

openerp.pos_done_order_load = function(instance, local) {


    var module = instance.point_of_sale;
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;

    /*************************************************************************
        New Widget LoadDoneOrderButtonWidget:
            * On click, display a new screen to select a Pos Order;
    */
    module.LoadDoneOrderButtonWidget = module.PosBaseWidget.extend({
        template: 'LoadDoneOrderButtonWidget',

        renderElement: function() {
            var self = this;
            this._super();
            this.$el.click(function(){
                var ss = self.pos.pos_widget.screen_selector;
                ss.set_current_screen('done_order_list');
            });
        },
    });


    /*************************************************************************
        Extend PosWidget:
            * Create new screen;
            * Add load button;
    */
    module.PosWidget = module.PosWidget.extend({
        build_widgets: function() {
            this._super();

            if (this.pos.config.iface_load_done_order){
                // New Screen to select a picking
                this.done_order_list_screen = new module.DoneOrderListScreenWidget(this, {});
                this.done_order_list_screen.appendTo(this.$('.screens'));
                this.done_order_list_screen.hide();
                this.screen_selector.screen_set.done_order_list = this.done_order_list_screen;

                // Add button
                this.load_done_order_button = new module.LoadDoneOrderButtonWidget(this,{});
                this.load_done_order_button.appendTo(this.pos_widget.$('li.orderline.empty'));
            }
        },
    });


    /*************************************************************************
        Extend OrderWidget:
    */
    module.OrderWidget = module.OrderWidget.extend({
        renderElement: function(scrollbottom){
            this._super(scrollbottom);
            if (this.pos_widget.load_done_order_button) {
                this.pos_widget.load_done_order_button.appendTo(
                    this.pos_widget.$('li.orderline.empty')
                );
            }
        }
    });


    /*************************************************************************
        New ScreenWidget DoneOrderListScreenWidget:
            * On show, display all done orders;
    */
    module.DoneOrderListScreenWidget = module.ScreenWidget.extend({
        template: 'DoneOrderListScreenWidget',
        show_leftpane: false,
        model: 'pos.order',

        start: function() {
            var self = this;
            this._super();

            // Bind click buttons
            this.$el.find('span.button.cancel').click(_.bind(this.clickCancelButton, this));

            // manage Search Box
            var search_timeout = null;
            this.$('.searchbox input').on('keyup',function(event){
                clearTimeout(search_timeout);
                var query = this.value;
                search_timeout = setTimeout(function(){
                    self.perform_search(query);
                },70);
            });

            this.$('.searchbox .search-clear').click(function(){
                self.clear_search();
            });
        },

        show: function() {
            this._super();
            this.perform_search();
        },

        // User Event
        clickCancelButton: function(event) {
            var ss = this.pos.pos_widget.screen_selector;
            ss.set_current_screen('products');
        },

        on_click_print_order: function(event){
            this.load_order(parseInt(event.target.parentNode.dataset.orderId, 10), 'print');
        },

        load_order: function(order_id, action) {
            var self = this;
            var posOrderModel = new instance.web.Model(this.model);
            return posOrderModel.call('load_done_order_for_pos', [[order_id]])
            .then(function (order_data) {
                var correct_order_print = true;
                var order = new module.Order({pos:self.pos});
                // Set Generic Info
                order.name = order_data.pos_reference;
                order.set_client(self.pos.db.get_partner_by_id(order_data.partner_id.id));

                // set order lines
                var orderLines = order_data.line_ids || [];
                var unknown_products = [];
                for (var i=0, len=orderLines.length; i<len; i++) {

                    var orderLine = orderLines[i];
                    
                    var product = self.pos.db.get_product_by_id(orderLine.product_id);
                    // check if product are available in pos
                    if (_.isUndefined(product)) {
                        unknown_products.push(line_name);
                    }
                    else{
                        // create a new order line
                        order.addProduct(product, {
                            price: orderLine.price_unit,
                            quantity: orderLine.quantity,
                            discount: orderLine.discount,
                            merge:false,
                        })
                    }
                }

                // Set Payment lines
                var paymentLines = order_data.statement_ids || [];
                _.each(paymentLines, function(paymentLine) {
                    var payment_found = false;
                    _.each(self.pos.cashregisters, function(cashregister) {
                        
                        if (cashregister.id === paymentLine.statement_id){
                            payment_found = true;
                            if (paymentLine.amount > 0){
                                // if it is not change
                                order.addPaymentline(cashregister);
                                order.selected_paymentline.set_amount(paymentLine.amount);
                            }
                        }
                    })
                    if (!payment_found && action === 'print'){
                        self.pos_widget.screen_selector.show_popup(
                            'error-traceback', {
                                message: _t('Unknown Statement'),
                                comment: _t("Unable to print this order because it doesn't belong to the current session ")
                            });
                        correct_order_print = false;
                    }

                })

                // Forbid POS Order loading if some products are unknown
                if (unknown_products.length > 0){
                    self.pos_widget.screen_selector.show_popup(
                        'error-traceback', {
                            message: _t('Unknown Products'),
                            comment: _t('Unable to load some order lines because the ' +
                                    'products are not available in the POS cache.\n\n' +
                                    'Please check that lines :\n\n  * ') + unknown_products.join("; \n  *")
                        });
                    correct_order_print = false;
                }


                if (correct_order_print){
                    var receipt = order.export_for_printing();
                    self.pos.proxy.print_receipt(QWeb.render('XmlReceipt', {
                        receipt: receipt, widget: self,
                    }));
                }

            }).fail(function (error, event){
                if (parseInt(error.code) === 200) {
                    // Business Logic Error, not a connection problem
                    self.pos_widget.screen_selector.show_popup(
                        'error-traceback', {
                            message: error.data.message,
                            comment: error.data.debug
                        });
                }
                else{
                    self.pos_widget.screen_selector.show_popup('error',{
                        message: _t('Connection error'),
                        comment: _t('Can not execute this action because the POS is currently offline'),
                    });
                }
                event.preventDefault();
            });
        },

        search_done_orders: function(query) {
            var self = this;
            var posOrderModel = new instance.web.Model(this.model);
            return posOrderModel.call('search_done_orders_for_pos', [query || '', this.pos.pos_session.id])
            .then(function (result) {
                self.render_list(result);
            }).fail(function (error, event){
                if (parseInt(error.code) === 200) {
                    // Business Logic Error, not a connection problem
                    self.pos_widget.screen_selector.show_popup(
                        'error-traceback', {
                            message: error.data.message,
                            comment: error.data.debug
                        }
                    );
                }
                else{
                    self.pos_widget.screen_selector.show_popup('error',{
                        message: _t('Connection error'),
                        comment: _t('Can not execute this action because the POS is currently offline'),
                    });
                }
                event.preventDefault();
            });
        },

        render_list: function(orders){
            var self = this;
            var contents = this.$el[0].querySelector('.done-order-list-contents');
            contents.innerHTML = "";
            var line_list = document.createDocumentFragment();
            _.each(orders, function(order){
                var order_line_html = QWeb.render('LoadDoneOrderLine', {widget: this, order: order});
                var order_line = document.createElement('tbody');
                order_line.innerHTML = order_line_html;
                order_line = order_line.childNodes[1];
                order_line.querySelector('.print-done-order').addEventListener('click', self.on_click_print_order);
                line_list.appendChild(order_line);
            });
            contents.appendChild(line_list);
        },

        perform_search: function(query){
            this.search_done_orders(query);
        },

        clear_search: function(){
            this.search_done_orders();
            this.$('.searchbox input')[0].value = '';
            this.$('.searchbox input').focus();
        },

    });

};
