'use strict';


angular.module('scan_to_purchase').controller(
        'SelectPurchaseOrderCtrl', [
        '$scope', '$rootScope', 'jsonRpc', '$state', 'PurchaseOrderModel',
        function ($scope, $rootScope, jsonRpc, $state, PurchaseOrderModel) {

    $scope.data = {
        'purchase_order_qty': 0,
        'purchase_order_list': false,
    }

    $scope.$on(
            '$stateChangeSuccess',
            function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'select_purchase_order') {
            $scope.data.purchase_order_list = $rootScope.DraftOrderList;
            $scope.data.purchase_order_qty = $rootScope.DraftOrderList.length;
        }
    });

    $scope.selectPurchaseOrder = function (id, name, partner_id) {
        $rootScope.currentPurchaseOrderId = id;
        $rootScope.currentPurchaseOrderName = name;
        $rootScope.currentPartnerId = partner_id;
        $state.go('select_product');
    };

    $scope.submit = function () {
        $state.go('select_supplier');
    };

}]);
