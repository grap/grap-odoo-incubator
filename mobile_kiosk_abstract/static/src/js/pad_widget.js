// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_abstract.pad_widget", function (require) {
    "use strict";

    var Widget = require('web.Widget');

    var PadWidget = Widget.extend({
        template: "MobileAppAbstract.PadWidget",

        events: {
            'click .kiosk-button-pad': function(event) {
                var key = event.target.attributes["data-value-id"].nodeValue;
                if (! isNaN(key)){
                    this.set_input_value(this.get_input_value() + key);
                } else if (key === "."){
                    if (this.$('#quantity').val().indexOf(".") === -1){
                        this.set_input_value(this.get_input_value() + key);
                    }
                } else if (key === "C"){
                    this.set_input_value("");
                }
            },
        },

        get_input_value: function(){
            return this.$('#quantity').val();
        },

        set_input_value: function(value){
            return this.$('#quantity').val(value);
        },

    });

    return PadWidget;

});
