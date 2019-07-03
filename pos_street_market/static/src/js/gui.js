/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('pos_street_market.gui', function (require) {
    "use strict";

    console.log("Loaded: gui");

    var gui = require('point_of_sale.gui');

    gui.Gui.include({

        select_market_place: function(options){
            console.log("market place");
            options = options || {};
            var self = this;
            var def  = new $.Deferred();

            var list = [];
            for (var i = 0; i < this.pos.users.length; i++) {
                var user = this.pos.users[i];
                if (!options.only_managers || user.role === 'manager') {
                    list.push({
                        'label': user.name,
                        'item':  user,
                    });
                }
            }

            this.show_popup('selection',{
                title: options.title || _t('Select User'),
                list: list,
                confirm: function(user){ def.resolve(user); },
                cancel: function(){ def.reject(); },
                is_selected: function(user){ return user === self.pos.get_cashier(); },
            });

            return def.then(function(user){
                if (options.security && user !== options.current_user && user.pos_security_pin) {
                    return self.ask_password(user.pos_security_pin).then(function(){
                        return user;
                    });
                } else {
                    return user;
                }
            });
        },

    });

});
