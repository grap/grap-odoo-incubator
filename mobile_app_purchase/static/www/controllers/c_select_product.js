'use strict';


angular.module('mobile_app_purchase').controller(
        'SelectProductCtrl', [
        '$scope', '$rootScope', 'jsonRpc', '$state', '$translate', 'PurchaseOrderModel',
        function ($scope, $rootScope, jsonRpc, $state, $translate, PurchaseOrderModel) {

    $scope.data = {
        'ean13': '',
    };

    $scope.$on(
            '$stateChangeSuccess',
            function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'select_product') {
            // Set Focus
            angular.element(document.querySelector('#input_ean13'))[0].focus();
            $scope.data.ean13 = '';

            // Load current Purchase orders
            PurchaseOrderModel.LoadOrder(
                    $rootScope.currentPurchaseOrderId).then(function (res){
                $scope.order = res;
            })
        }
    });

    $scope.submit = function () {
        if ($scope.data.ean13 in $rootScope.ProductListByEan13){
            $scope.errorMessage = "";
            $state.go('select_quantity', {ean13: $scope.data.ean13});
        }else{
            $scope.errorMessage = $translate.instant("Unknown EAN13 Barcode");
            angular.element(document.querySelector('#sound_user_error'))[0].play();
        }
    };

}]);
