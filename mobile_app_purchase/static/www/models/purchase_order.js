// Copyright (C) 2015-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
//  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"use strict";

angular.module('mobile_app_purchase').factory(
        'PurchaseOrderModel', [
        '$q', 'jsonRpc',
        function ($q, jsonRpc) {

    return {
        get_list: function() {
            //always a fresh list
            return jsonRpc.call(
                    'mobile.app.purchase', 'get_purchase_orders', []).then(function (res) {
                return res;
            });
        },

        get_purchase_order: function(id) {
            return this.get_list().then(function (purchase_orders) {
                var found = false;
                purchase_orders.some(function(purchase_order) {
                    if (purchase_order.id != id)
                        return false;
                    found = purchase_order;
                    return;
                });
                return found || $q.reject('Purchase Order not found');
            });
        },

        create_purchase_order: function(partner) {
            var vals = {'partner': partner}
            return jsonRpc.call('mobile.app.purchase', 'create_purchase_order', [vals]).then(function(purchase_order){
                return purchase_order;
            });
        },

        add_purchase_order_line: function(purchase_order, product, quantity) {
            var vals = {
                'purchase_order': purchase_order,
                'product': product,
                'qty': quantity,
            }
            return jsonRpc.call(
                    'mobile.app.purchase', 'add_purchase_order_line', [vals]).then(function (res) {
                return res;
            });
        },

    };
}]);
