'use strict';


angular.module('scan_to_purchase').controller(
        'SelectQuantityCtrl',
        ['$scope', '$rootScope', 'jsonRpc', '$state', 'PurchaseOrderModel', '$translate',
        function ($scope, $rootScope, jsonRpc, $state, PurchaseOrderModel, $translate) {

    $scope.data = {
        'qty': '',
    };

    $scope.$on(
            '$stateChangeSuccess',
            function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'select_quantity') {
            // Set Focus
            angular.element(document.querySelector('#input_quantity'))[0].focus();

            // Get Product Data
            $scope.product = $rootScope.ProductListByEan13[toParams['ean13']];
        }
    });

    $scope.submit = function () {
        if ($scope.data.qty != null && !isNaN($scope.data.qty)){
            if ($scope.data.qty < 1000000){
                if ($scope.data.qty > 0){
                    PurchaseOrderModel.AddOrderLine(
                            $rootScope.currentPurchaseOrderId, $scope.product.id,
                            $scope.data.qty).then(function (res){
                        angular.element(document.querySelector('#sound_quantity_selected'))[0].play();
                        setTimeout(function(){
                            $state.go('select_product');
                        }, 300);
                    }, function(reason) {
                        $scope.errorMessage = $translate.instant("Something Wrong Happened");
                    });
                }else{
                    $scope.errorMessage = $translate.instant("Too Small Quantity");
                    angular.element(document.querySelector('#sound_user_error'))[0].play();
                }
            }else{
                $scope.errorMessage = $translate.instant("Too Big Quantity");
                    angular.element(document.querySelector('#sound_user_error'))[0].play();
            }
        }
        else{
            $scope.errorMessage = $translate.instant("Incorrect Quantity");
            angular.element(document.querySelector('#sound_user_error'))[0].play();
        }
    };

}]);
