// Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
// Copyright (C) 2022 - Today: Coop IT Easy SC
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// @author: Carmen Bianca Bakker
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("pos_wallet.screens", function (require) {
    "use strict";

    var screens = require("point_of_sale.screens");
    var core = require('web.core');
    var _t = core._t;


    screens.PaymentScreenWidget.include({

        customer_changed: function () {
            this._super();
            if (this.pos.config.is_enabled_wallet) {
                var client = this.pos.get_client();
                this.$(".balance").text(
                    client ? this.format_currency(client.wallet_balance) : ""
                );
            }
        },

        click_paymentmethods: function(id) {
            var cashregister = null;
            for ( var i = 0; i < this.pos.cashregisters.length; i++ ) {
                if ( this.pos.cashregisters[i].journal_id[0] === id ){
                    cashregister = this.pos.cashregisters[i];
                    break;
                }
            }
            if (cashregister.journal.is_wallet && ! this.pos.get_order().get_client()) {
                this.gui.show_popup('error',{
                    'title': _t('No Client'),
                    'body':  _t('To select a wallet payment method, you should have a customer selected'),
                });
                return;
            }

            return this._super.apply(this, arguments);
        },

        validate_order: function(options) {

            // Check if a wallet journal is selected
            var has_wallet_journal = false;

            this.pos.get_order().paymentlines.forEach(function (paymentline) {
                if (paymentline.cashregister.journal.is_wallet) {
                    has_wallet_journal = true;
                }
            });
            if (has_wallet_journal && !this.pos.get_order().get_client()){
                this.gui.show_popup('error',{
                    'title': _t('No Client'),
                    'body':  _t('To select a wallet payment method, you should have a customer selected'),
                });
                return;
            }

            // Check if a wallet journal is selected
            var has_wallet_product = false;
            var wallet_product_ids = [];

            this.pos.wallet_types.forEach(function (wallettype) {
                wallet_product_ids.push(wallettype.product_id[0]);
            })
            this.pos.get_order().orderlines.forEach(function (orderline) {
                if (wallet_product_ids.includes(orderline.product.id)){
                    has_wallet_product = true
                }
            });
            if (has_wallet_product && !this.pos.get_order().get_client()){
                this.gui.show_popup('error',{
                    'title': _t('No Client'),
                    'body':  _t('To sell a Wallet product, you should have a customer selected'),
                });
                return;
            }

            return this._super(options);
        }

    });

});
