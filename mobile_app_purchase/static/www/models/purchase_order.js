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

        // create_inventory: function(name) {
        //     var vals = {'inventory': {'name': name}}
        //     return jsonRpc.call('mobile.app.inventory', 'create_inventory', [vals]).then(function(inventory){
        //         return inventory;
        //     });
        // },

        // add_inventory_line: function(inventory, location, product, quantity, mode) {
        //     var vals = {
        //         'inventory': {'id': inventory.id},
        //         'location': {'id': location.id},
        //         'product': {'id': product.id, 'barcode': product.barcode},
        //         'qty': quantity,
        //         'mode': mode,
        //     }
        //     return jsonRpc.call(
        //             'mobile.app.inventory', 'add_inventory_line', [vals]).then(function (res) {
        //         return res;
        //     });
        // },

    };
}]);








// 'use strict';


// angular.module('mobile_app_purchase').factory(
//         'PurchaseOrderModel', [
//         '$q', '$rootScope', 'jsonRpc',
//         function ($q, $rootScope, jsonRpc) {

//     return {
//         LoadDraftOrder: function() {
//             return jsonRpc.searchRead(
//                     'purchase.order', [['state', '=', 'draft']], [
//                     'id', 'name', 'partner_id', 'amount_untaxed',
//                     'amount_total', 'minimum_planned_date',
//                     ]).then(function (res) {
//                 $rootScope.DraftOrderList = res.records;
//                 return res.records.length;
//             });
//         },
//         CreatePurchaseOrder: function(partnerId) {
//             return jsonRpc.call(
//                     'mobile.app.purchase', 'create_purchase_order',
//                     [partnerId]).then(function (res) {
//                 return res;
//             });
//         },
//         LoadOrder: function(orderId) {
//             return jsonRpc.searchRead(
//                     'purchase.order', [['id', '=', orderId]], [
//                     'id', 'name', 'partner_id', 'amount_untaxed',
//                     'amount_total',
//                     ]).then(function (res) {
//                 return res.records[0];
//             });
//         },
//         AddOrderLine: function(purchaseOrderId, productId, quantity) {
//             return jsonRpc.call(
//                     'mobile.app.purchase', 'add_purchase_order_line',
//                     [purchaseOrderId, productId, quantity]).then(function (res) {
//                 return res;
//             });
//         },

//     };
// }]);
