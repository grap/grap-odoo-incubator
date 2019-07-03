/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('pos_street_market.models', function (require) {
    "use strict";

    console.log("Loaded: models");

    var models = require('point_of_sale.models');

    // Load market.place model
    models.load_models({
        model: 'market.place',
        loaded: function(self,market_places){
            self.market_places_by_id = {};
            for (var i = 0; i < market_places.length; i++) {
                self.market_places_by_id[market_places[i].id] = market_places[i];
            }
            console.log(self.market_places_by_id);

        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
    });

});
    // initialize: function() {
    //     _super_order.initialize.apply(this,arguments);
    //     if (!this.table) {
    //         this.table = this.pos.table;
    //     }
    //     this.customer_count = this.customer_count || 1;
    //     this.save_to_db();
    // },
    // export_as_JSON: function() {
    //     var json = _super_order.export_as_JSON.apply(this,arguments);
    //     json.table     = this.table ? this.table.name : undefined;
    //     json.table_id  = this.table ? this.table.id : false;
    //     json.floor     = this.table ? this.table.floor.name : false;
    //     json.floor_id  = this.table ? this.table.floor.id : false;
    //     json.customer_count = this.customer_count;
    //     return json;
    // },
    // init_from_JSON: function(json) {
    //     _super_order.init_from_JSON.apply(this,arguments);
    //     this.table = this.pos.tables_by_id[json.table_id];
    //     this.floor = this.table ? this.pos.floors_by_id[json.floor_id] : undefined;
    //     this.customer_count = json.customer_count || 1;
    // },
    // export_for_printing: function() {
    //     var json = _super_order.export_for_printing.apply(this,arguments);
    //     json.table = this.table ? this.table.name : undefined;
    //     json.floor = this.table ? this.table.floor.name : undefined;
    //     json.customer_count = this.get_customer_count();
    //     return json;
    // },





// function load__pos_street_market__models(instance) {
// "use strict";

//     var module = instance.point_of_sale;

// /* ****************************************************************************
// Overload: point_of_sale.PosModel

// - Overload module.PosModel.initialize function to load extra-data
//      - Load 'market.place' model;
// **************************************************************************** */

//     var _initialize_ = module.PosModel.prototype.initialize;
//     module.PosModel.prototype.initialize = function(session, attributes){
//         // Load Market Place
//         var model = {
//             model: 'market.place',
//             fields: ['code', 'name'],
//             loaded: function(self, market_places){
//                  self.db.add_market_places(market_places);
//             },
//         };
//         this.models.push(model);

//         return _initialize_.call(this, session, attributes);
//     };
// /* ****************************************************************************
// Overload: point_of_sale.Order

// - send to server the selected Market Place
// **************************************************************************** */

//     var _export_as_JSON_original = module.Order.prototype.export_as_JSON;

//     module.Order.prototype.export_as_JSON = function(){
//         var res = _export_as_JSON_original.call(this);
//         res.market_place_id = this.pos.current_market_place_id;
//         return res;
//     };

// }
