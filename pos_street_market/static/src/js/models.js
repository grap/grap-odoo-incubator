/******************************************************************************
    Point Of Sale - Street Market module for Odoo
    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
    @author Sylvain LE GAL (https://twitter.com/legalsylvain)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
******************************************************************************/

function load__pos_street_market__models(instance) {

    module = instance.point_of_sale;

/* ****************************************************************************
Overload: point_of_sale.PosModel

- Overload module.PosModel.initialize function to load extra-data
     - Load 'market.place' model;
**************************************************************************** */

    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        self = this;

        // Load Market Place
        model = {
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
