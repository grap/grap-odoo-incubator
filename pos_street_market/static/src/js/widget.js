/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('pos_street_market.widgets', function (require) {
    "use strict";

    var chrome = require('point_of_sale.chrome');
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var core = require('web.core');
    var _t = core._t;

    var MarketPlaceNameWidget = PosBaseWidget.extend({
        template: 'MarketPlaceNameWidget',
        init: function(parent, options){
            options = options || {};
            this._super(parent,options);
        },
        renderElement: function(){
            var self = this;
            this._super();

            this.$el.click(function(){
                self.click_market_place();
            });
        },
        click_market_place: function(){
            console.log("click_market_place");
            var self = this;
            this.gui.select_market_place({
                'security':     true,
                'current_market_place': this.pos.get_market_place(),
                'title':      _t("Change Market Place"),
            }).then(function(market_place){
                self.pos.set_market_place(market_place);
                self.renderElement();
            });
        },
        get_name: function(){
            var market_place = this.pos.get_market_place();
            if(market_place){
                return market_place.code;
            }else{
                return _t("Market Place");
            }
        },
    });

    return {
        MarketPlaceNameWidget: MarketPlaceNameWidget,
    };

});
