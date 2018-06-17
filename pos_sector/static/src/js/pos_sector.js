/*
Copyright (C) 2018-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

"use strict";

openerp.pos_sector = function(instance){
    var module = instance.point_of_sale;

    var PosModelParent = module.PosModel;
    module.PosModel = module.PosModel.extend({

        initialize: function (session, attributes) {
            PosModelParent.prototype.initialize.apply(this, arguments);

            var product_product_model = false;
            for (var i = 0, len = this.models.length; i < len; i++) {
                if (this.models[i].model === 'product.product') {
                    product_product_model = this.models[i];
                }
            }
            if (product_product_model){
                this.domain_before_pos_sector = product_product_model.domain;
                product_product_model.domain = function(self){
                    var new_domain = self.domain_before_pos_sector;
                    new_domain.push('|', ['sector_id', '=', false], ['sector_id', 'in', self.config.sector_ids]);
                    return new_domain;
                };
            }
        },
    });
};
