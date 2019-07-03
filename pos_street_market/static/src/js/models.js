/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('pos_street_market.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;


    // Load market.place model
    models.load_models({
        model: 'market.place',
        loaded: function(self, market_places){
            self.market_places = [];
            for (var i = 0; i < market_places.length; i++) {
                self.market_places.push(market_places[i]);
            }
        },
    });

    // make market place persistent in the session
    models.PosModel = models.PosModel.extend({
        get_market_place: function(){
            return this.get('current_market_place') || this.db.load('current_market_place');
        },
        set_market_place: function(market_place){
            this.set('current_market_place', market_place);
            this.db.save('current_market_place', market_place || null);
        },
    });

    // Add market place to JSON
    models.Order = models.Order.extend({
        export_as_JSON: function() {
            var json = _super_order.export_as_JSON.apply(this, arguments);
            var market_place = this.pos.get_market_place();
            json.market_place_id = market_place ? market_place.id : false;
            return json;
        },
    });

});
