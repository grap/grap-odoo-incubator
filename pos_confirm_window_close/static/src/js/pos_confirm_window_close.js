/*
Copyright (C) 2017-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

"use strict";

openerp.pos_confirm_window_close = function(instance){
    var module = instance.point_of_sale;

    module.PosWidget = module.PosWidget.extend({
        start: function() {
            // Prevent History back
            window.addEventListener("popstate", function() {
                history.pushState(null, null, document.URL);
            });

            // Prevent closing window
            window.addEventListener("beforeunload", function(e) {
                var confirmationMessage = instance.web._t(
                    "You could have unsaved data in this window. " +
                    "Do you really want to leave?");
                e.returnValue = confirmationMessage;
                return confirmationMessage;
            });
            return this._super();
        },
    });
};
