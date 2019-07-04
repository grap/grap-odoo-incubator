/**
Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('pos_street_market.chrome', function (require) {
    "use strict";

    var chrome = require('point_of_sale.chrome');
    var pos_street_market_widget = require('pos_street_market.widgets');

    chrome.Chrome.include({

        init: function() { 
            var self = this;
            this.widgets.push({
                'name':     'market_place_name',
                'widget':   pos_street_market_widget.MarketPlaceNameWidget,
                'replace':  '.placeholder-MarketPlaceNameWidget',
            },);
            this._super(arguments[0], {});
        },

    });

});
