/*
Copyright (C) 2015-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

odoo.define('pos_manual_weight_entry.screens', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    screens.ScaleScreenWidget.include({

        // // /////////////////////////////
        // // Overload Section
        // // /////////////////////////////
        show: function(){
            this._super();
            this.manual_gross_weight_ok = true;
            this.set_manual_mode();
            var self = this;
            this.$('#input_gross_weight').keyup(function(event){
                self.onchange_gross_weight(event);
            });
            this.$('#input_gross_weight').focus()
        },

        order_product: function(){
            if (!this.manual_gross_weight_ok) {
                this.gui.show_popup('error',{
                    'title': _t('Incorrect Weight Value'),
                    'body': _t('Please set a numeric value in the Weight field.'),
                });
            }
            else {
                this._super();
            }
        },

        // // /////////////////////////////
        // // Custom Section
        // // /////////////////////////////
        set_manual_mode: function(){
            this.$('#container_weight_gross').css("display", "none");
            // disable the read of the value from the scale
            this.pos.proxy_queue.clear();
        },

        onchange_gross_weight: function(event){
            var gross_weight = this.check_sanitize_value('#input_gross_weight');
            this.manual_gross_weight_ok = !isNaN(gross_weight);
            this.set_weight(gross_weight);
        },

    });

});
