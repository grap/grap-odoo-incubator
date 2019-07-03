/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('pos_street_market.gui', function (require) {
    "use strict";

    var gui = require('point_of_sale.gui');

    gui.Gui.include({

        select_market_place: function(options){
            var self = this;
            var def  = new $.Deferred();

            var list = [];
            for (var i = 0; i < this.pos.market_places.length; i++) {
                var market_place = this.pos.market_places[i];
                list.push({
                    'label': market_place.code + " - " + market_place.name,
                    'item':  market_place,
                });
            }

            this.show_popup('selection',{
                list: list,
                confirm: function(market_place){
                    def.resolve(market_place);
                },
                cancel: function(){
                    def.resolve(null);
                },
                is_selected: function(market_place){ return market_place === self.pos.get_market_place(); },
            });

            return def.then(function(market_place){
                return market_place;
            });
        },

    });

});
