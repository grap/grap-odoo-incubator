"use strict";
angular.module('mobile_app_purchase').controller(
    'PurchaseOrderCtrl', [
    '$scope', '$state', 'PurchaseOrderModel', 'ProductModel', '$translate',
    function ($scope, $state,  PurchaseOrderModel, ProductModel, $translate) {

    $scope.data = {
        'purchase_order_list': [],
        'purchase_order_filter': null,
    };

    $scope.$on(
        '$stateChangeSuccess',
        function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'purchase_order') {
            $scope.data.inventory_filter = null;
            PurchaseOrderModel.get_list().then(function (purchase_order_list) {
                $scope.data.purchase_order_list = purchase_order_list;
            });
        }
    });

    $scope.create_purchase_order = function () {
        $state.go('partner');
    };

    $scope.select_purchase_order = function (purchase_order_id) {
        // Load Products
        ProductModel.get_list(purchase_order).then(function(product_list) {
            $state.go('product', {purchase_order_id: purchase_order_id});
        });
    };
}]);



// 'use strict';


// angular.module('mobile_app_purchase').controller(
//         'SelectPurchaseOrderCtrl', [
//         '$scope', '$rootScope', 'jsonRpc', '$state', 'PurchaseOrderModel',
//         function ($scope, $rootScope, jsonRpc, $state, PurchaseOrderModel) {

//     $scope.data = {
//         'purchase_order_qty': 0,
//         'purchase_order_list': false,
//     }

//     $scope.$on(
//             '$stateChangeSuccess',
//             function(event, toState, toParams, fromState, fromParams){
//         if ($state.current.name === 'select_purchase_order') {
//             $scope.data.purchase_order_list = $rootScope.DraftOrderList;
//             $scope.data.purchase_order_qty = $rootScope.DraftOrderList.length;
//         }
//     });

//     $scope.selectPurchaseOrder = function (id, name, partner_id) {
//         $rootScope.currentPurchaseOrderId = id;
//         $rootScope.currentPurchaseOrderName = name;
//         $rootScope.currentPartnerId = partner_id;
//         $state.go('select_product');
//     };

//     $scope.submit = function () {
//         $state.go('select_supplier');
//     };

// }]);
