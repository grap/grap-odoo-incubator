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

function load__pos_street_market__db(instance) {

    module = instance.point_of_sale;

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
                var attribute_value_ids = [];
                // store Market Places
                this.market_places.push(market_places[i]);
            }
        },

    });
}
