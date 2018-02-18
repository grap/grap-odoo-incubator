/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

function load__pos_street_market__widget(instance) {
"use strict";

    var module = instance.point_of_sale;
    var _t = instance.web._t;

/* ****************************************************************************
Overload: point_of_sale.PosWidget

- Add a new PopUp select_market_place_popup in the PopUp List;
**************************************************************************** */

    module.PosWidget = module.PosWidget.extend({

        /* Overload Section */
        build_widgets: function(){
            this._super();

            var self = this;

            // Create new PopUp
            this.select_market_place_popup = new module.SelectMarketPlacePopupWidget(this, {});
            this.select_market_place_popup.appendTo($(this.$el));

            // Hide the popup because all new PopUp are displayed by default
            this.select_market_place_popup.hide();

            // Add the New PopUp to the screen selector
            this.screen_selector.popup_set['select-market-place-popup'] = this.select_market_place_popup;

            // Add On click behaviour to display the PopUp
            if (this.pos.config.iface_street_market){
                this.$('#button_select_market_place').click(function () {
                    self.screen_selector.show_popup('select-market-place-popup');
                });
            } else{
                this.$('#button_select_market_place').hide();
            }
        },

    });

/* ****************************************************************************
Define : pos_street_market.SelectMarketPlacePopupWidget

- This widget display a pop up to select a Market Place that will be used for
  all the next PoS Orders;
- Add the possibility to unset a selecte Market Place;
**************************************************************************** */

    module.SelectMarketPlacePopupWidget = module.PopUpWidget.extend({
        template:'SelectMarketPlacePopupWidget',

        /* Overload Section */
        start: function(){
            this._super();
            var self = this;

            // Add List Screen Widget
            this.market_place_list_screen_widget = new module.MarketPlaceListScreenWidget(this,{});
            this.market_place_list_screen_widget.renderElement();
            this.market_place_list_screen_widget.replace($('.placeholder-MarketPlaceListScreenWidget'));

            // Add On click behaviour to hide the PopUp
            this.$('#market-place-empty').click(function () {
                self.pos.current_market_place_id = false;
                self.pos_widget.$('#button_select_market_place')[0].innerHTML = _t('Market Place');
                self.pos_widget.$('#button_select_market_place').removeClass('selected');
                self.pos_widget.screen_selector.close_popup();
            });
        },
    });

/* ****************************************************************************
Define : pos_street_market.MarketPlaceListScreenWidget

- Display a list of market places;
**************************************************************************** */
    module.MarketPlaceListScreenWidget = module.ScreenWidget.extend({
        template:'MarketPlaceListScreenWidget',

        /* Overload Section */
        start: function() {
            this._super();

            // Display Market Places list
            var market_places = this.pos.db.market_places;

            for(var i = 0, len = market_places.length; i < len; i++){
                var market_place_widget = new module.MarketPlaceWidget(this, {
                    model: market_places[i],
                });
                market_place_widget.appendTo(this.$('.market-place-widget-list'));
            }
        },
    });

/* ****************************************************************************
Define : pos_street_market.MarketPlaceWidget

- Display a market place;
**************************************************************************** */
    module.MarketPlaceWidget = module.PosBaseWidget.extend({
        template: 'MarketPlaceWidget',

        /* Overload Section */
        init: function(parent, options) {
            this._super(parent, options);
            this.model = options.model;
        },

        renderElement: function() {
            this._super();
            var self = this;
            $("a", this.$el).click(function(e){
                self.pos.current_market_place_id = self.model.id;
                self.pos_widget.$('#button_select_market_place')[0].innerHTML = self.model.code;
                self.pos_widget.$('#button_select_market_place').addClass('selected');
                self.pos_widget.screen_selector.close_popup();
            });
        },
    });

}
