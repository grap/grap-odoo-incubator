// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_abstract.widget", function (require) {
    "use strict";

    var Widget = require('web.Widget');

    Widget.include({

        kiosk_update_context_from_result: function(context, result){
            Object.keys(result).forEach(function(key){
                if (key !== "status" && key !== "messages"){
                    context[key] = result[key];
                }
            });
        },

        kiosk_warn_connexion: function(){
            this.do_warn(
                _t("Connexion lost"),
                _t("Please check your Internet Connexion, then try again"),
                false
            );
        },

        kiosk_notify_result: function(result){
            var self = this;
            var messages = result["messages"] || [];
            messages.forEach(function(message){
                if (message.level === "error"){
                    self.do_warn(message.title, message.message, false);
                } else {
                    self.do_notify(message.title, message.message, false);
                }
            });

        },

    });
});
