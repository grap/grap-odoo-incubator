// Copyright (C) 2020-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("mobile_kiosk_inventory.inventory_action", function (require) {
    "use strict";

    var ActionMobileKioskAbstract = require("mobile_kiosk_abstract.abstract_action");

    var ActionMobileKioskInventory = ActionMobileKioskAbstract.extend({

        _kiosk_home_page_tag: "mobile_kiosk_inventory_action_set_inventory",
        _kiosk_home_page_name: "Inventory",

        _kiosk_title: "Inventory your Stock",

    });

    return ActionMobileKioskInventory;

});
