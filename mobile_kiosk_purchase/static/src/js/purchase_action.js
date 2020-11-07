// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_purchase.purchase_action", function (require) {
    "use strict";

    var core = require('web.core');
    var ActionMobileKioskAbstract = require("mobile_kiosk_abstract.abstract_action");
    var _t = core._t;

    var ActionMobileKioskPurchase = ActionMobileKioskAbstract.extend({

        _kiosk_home_page_tag: "mobile_kiosk_purchase_action_set_supplier",
        _kiosk_home_page_name: _("Purchase"),

        _kiosk_title: _("Purchase Order"),

    });

    return ActionMobileKioskPurchase;

});
