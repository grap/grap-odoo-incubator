'use strict';


angular.module('mobile_app_purchase').controller(
        'SelectSupplierCtrl', [
        '$scope', '$rootScope', 'jsonRpc', '$state', 'PurchaseOrderModel',
        function ($scope, $rootScope, jsonRpc, $state, PurchaseOrderModel) {

    $scope.data = {
        'supplier_qty': 0,
        'supplier_list': false,
    }

    $scope.$on(
            '$stateChangeSuccess',
            function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'select_supplier') {
            $scope.data.supplier_list = $rootScope.SupplierList;
            $scope.data.supplier_qty = $rootScope.SupplierList.length;
        }
    });

    $scope.selectSupplier = function (partner_id) {
        PurchaseOrderModel.CreatePurchaseOrder(partner_id).then(function(order_res){
            $rootScope.currentPartnerId = partner_id;
            $rootScope.currentPurchaseOrderId = order_res;
            $state.go('select_product');
        });
    };

}]);
