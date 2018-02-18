/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

function load__pos_street_market__db(instance) {
"use strict";

    var module = instance.point_of_sale;

/* ****************************************************************************
Overload: point_of_sale.PosDB

- Add to local storage Market Places Data.
**************************************************************************** */

    module.PosDB = module.PosDB.extend({
        init: function(options){
            this.current_market_place_id = false;
            this.market_places = [];
            this._super(options);
        },

        add_market_places: function(market_places){
            for(var i=0 ; i < market_places.length; i++){
                this.market_places.push(market_places[i]);
            }
        },

    });
}
