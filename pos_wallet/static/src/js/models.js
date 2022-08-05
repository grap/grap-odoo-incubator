// Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define("pos_wallet.models", function (require) {
    "use strict";

    var models = require("point_of_sale.models");

    models.load_fields("res.partner", ["wallet_balance"]);

    models.load_fields("account.journal", ["is_wallet"]);

    // Load account.wallet.type model
    models.load_models({
        model: 'account.wallet.type',
        loaded: function (self, wallet_types) {
            self.wallet_types = [];
            for (var i = 0; i < wallet_types.length; i++) {
                self.wallet_types.push(wallet_types[i]);
            }
        },
    });

});
