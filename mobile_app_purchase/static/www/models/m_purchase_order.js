'use strict';


angular.module('scan_to_purchase').factory(
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
                    'purchase.order', 'create_order_by_scan',
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
                    'purchase.order', 'add_order_line_by_scan',
                    [purchaseOrderId, productId, quantity]).then(function (res) {
                return res;
            });
        },

    };
}]);
