"use strict";
angular.module('mobile_app_purchase').controller(
    'PartnerCtrl', [
    '$scope', '$filter', '$state', '$stateParams','PartnerModel', 'PurchaseOrderModel', 'ProductModel',
    function ($scope, $filter, $state, $stateParams, PartnerModel, PurchaseOrderModel, ProductModel) {
    $scope.data = {
        'partner_list': [],
        'partner_filter': null,
    };

    $scope.$on(
        '$stateChangeSuccess',
        function(event, toState, toParams, fromState, fromParams) {
        if ($state.current.name === 'partner') {
            $scope.data.partner_filter = null;
            PartnerModel.get_list().then(function(partner_list) {
                $scope.data.partner_list = partner_list;
            });
        }
    });

    $scope.select_partner = function (partner) {
        // Create Purchase order
        PurchaseOrderModel.create_purchase_order(partner).then(function(purchase_order){
            // Load Products
            ProductModel.get_list(purchase_order).then(function(product_list) {
                $state.go('product', {purchase_order_id: purchase_order.id});
            });
        });

    };

}]);





// 'use strict';


// angular.module('mobile_app_purchase').controller(
//         'SelectSupplierCtrl', [
//         '$scope', '$rootScope', 'jsonRpc', '$state', 'PurchaseOrderModel',
//         function ($scope, $rootScope, jsonRpc, $state, PurchaseOrderModel) {

//     $scope.data = {
//         'supplier_qty': 0,
//         'supplier_list': false,
//     }

//     $scope.$on(
//             '$stateChangeSuccess',
//             function(event, toState, toParams, fromState, fromParams){
//         if ($state.current.name === 'select_supplier') {
//             $scope.data.supplier_list = $rootScope.SupplierList;
//             $scope.data.supplier_qty = $rootScope.SupplierList.length;
//         }
//     });

//     $scope.selectSupplier = function (partner_id) {
//         PurchaseOrderModel.CreatePurchaseOrder(partner_id).then(function(order_res){
//             $rootScope.currentPartnerId = partner_id;
//             $rootScope.currentPurchaseOrderId = order_res;
//             $state.go('select_product');
//         });
//     };

// }]);
