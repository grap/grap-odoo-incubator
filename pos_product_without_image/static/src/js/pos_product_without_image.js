/******************************************************************************
    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
    @author Julien WESTE
    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
******************************************************************************/

"use strict";

openerp.pos_product_without_image = function(instance){
    var module = instance.point_of_sale;

    module.ProductListWidget = module.ProductListWidget.extend({
        get_product_image_url: function(product){
            if (product.has_image){
                return this._super(product);
            }
            return '/pos_product_without_image/static/src/img/placeholder_invisible.png';
        },

        render_product: function(product){
            var cached = this.product_cache.get_node(product.id);
            if(!cached){
                var res = this._super(product);
                if (!(product.has_image)){
                    res.children[1].classList.add('product-name-without-image');
                    // update cache
                    this.product_cache.cache_node(product.id, res);
                }
                return res;
            }
            return cached;
        },
    });

};
