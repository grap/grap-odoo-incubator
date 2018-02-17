/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

function load__pos_street_market__models(instance) {
"use strict";

    var module = instance.point_of_sale;

/* ****************************************************************************
Overload: point_of_sale.PosModel

- Overload module.PosModel.initialize function to load extra-data
     - Load 'market.place' model;
**************************************************************************** */

    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        var self = this;

        // Load Market Place
        var model = {
            model: 'market.place',
            fields: ['code', 'name'],
            loaded: function(self, market_places){
                 self.db.add_market_places(market_places);
            },
        }
        this.models.push(model);

        return _initialize_.call(this, session, attributes);
    };
/* ****************************************************************************
Overload: point_of_sale.Order

- send to server the selected Market Place
**************************************************************************** */

    var _export_as_JSON_original = module.Order.prototype.export_as_JSON;

    module.Order.prototype.export_as_JSON = function(){
        res = _export_as_JSON_original.call(this);
        res.market_place_id = this.pos.current_market_place_id;
        return res;
    };

}
