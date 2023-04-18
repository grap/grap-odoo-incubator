// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.inventory_action", function (require) {
    "use strict";

    var core = require("web.core");
    var ActionMobileKioskAbstract = require("mobile_kiosk_abstract.abstract_action");
    var _t = core._t;

    var ActionMobileKioskInventory = ActionMobileKioskAbstract.extend({

        _kiosk_home_page_tag: "mobile_kiosk_inventory_action_set_inventory",
        _kiosk_home_page_name: _t("Inventory"),

        _kiosk_title: _t("Inventory your Stock"),

    });

    return ActionMobileKioskInventory;

});
