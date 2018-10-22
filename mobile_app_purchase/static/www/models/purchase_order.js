'use strict';


angular.module('mobile_app_purchase').factory(
        'PurchaseOrderModel', [
        '$q', '$rootScope', 'jsonRpc',
        function ($q, $rootScope, jsonRpc) {

    return {
        LoadDraftOrder: function() {
            return jsonRpc.searchRead(
                    'purchase.order', [['state', '=', 'draft']], [
                    'id', 'name', 'partner_id', 'amount_untaxed',
                    'amount_total', 'minimum_planned_date',
                    ]).then(function (res) {
                $rootScope.DraftOrderList = res.records;
                return res.records.length;
            });
        },
        CreatePurchaseOrder: function(partnerId) {
            return jsonRpc.call(
                    'mobile.app.purchase', 'create_purchase_order',
                    [partnerId]).then(function (res) {
                return res;
            });
        },
        LoadOrder: function(orderId) {
            return jsonRpc.searchRead(
                    'purchase.order', [['id', '=', orderId]], [
                    'id', 'name', 'partner_id', 'amount_untaxed',
                    'amount_total',
                    ]).then(function (res) {
                return res.records[0];
            });
        },
        AddOrderLine: function(purchaseOrderId, productId, quantity) {
            return jsonRpc.call(
                    'mobile.app.purchase', 'add_purchase_order_line',
                    [purchaseOrderId, productId, quantity]).then(function (res) {
                return res;
            });
        },

    };
}]);
