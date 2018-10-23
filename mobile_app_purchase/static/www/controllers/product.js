"use strict";
angular.module('mobile_app_purchase').controller(
        'ProductCtrl', [
        '$scope', '$state', '$translate', 'PurchaseOrderModel', 'ProductModel',
        function ($scope, $state, $translate, PurchaseOrderModel, ProductModel) {

    $scope.data = { };

    $scope.$on(
            '$stateChangeSuccess',
            function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'product') {
            // Set Focus
            angular.element(document.querySelector('#input_ean13'))[0].focus();
            //Initialize default data
            $scope.data.ean13 = '';
            $scope.errorMessage = "";
            // Get Purchase order Data
            PurchaseOrderModel.get_purchase_order(toParams.purchase_order_id).then(function (purchase_order) {
                $scope.purchase_order = purchase_order;
            });
        }
    });

    $scope.submit = function () {
        // Reset Focus, in case the barcode is not correct
        angular.element(document.querySelector('#input_ean13'))[0].focus();
        if ($scope.data.ean13) {
            console.log("ean13");
            ProductModel.search_product($scope.data.ean13).then(function (product) {
                console.log("search_product result");
                if (!product.id){
                    console.log("not found");
                    $scope.errorMessage = $translate.instant("Unknown EAN13 Barcode");
                    angular.element(document.querySelector('#sound_error'))[0].play();
                } else {
                    console.log("found");
                    $state.go('quantity', {
                        purchase_order_id: $scope.purchase_order.id,
                        ean13: product.barcode,
                    });
                }
            });
        } else {
            $scope.errorMessage = $translate.instant("Barcode : Required field");
            angular.element(document.querySelector('#sound_error'))[0].play();
       }
    };

}]);




// 'use strict';


// angular.module('mobile_app_purchase').controller(
//         'ProductCtrl', [
//         '$scope', '$rootScope', 'jsonRpc', '$state', '$translate', 'PurchaseOrderModel',
//         function ($scope, $rootScope, jsonRpc, $state, $translate, PurchaseOrderModel) {

//     $scope.data = {
//         'ean13': '',
//     };

//     $scope.$on(
//             '$stateChangeSuccess',
//             function(event, toState, toParams, fromState, fromParams){
//         if ($state.current.name === 'product') {
//             // Set Focus
//             angular.element(document.querySelector('#input_ean13'))[0].focus();
//             $scope.data.ean13 = '';

//             // Load current Purchase orders
//             PurchaseOrderModel.LoadOrder(
//                     $rootScope.currentPurchaseOrderId).then(function (res){
//                 $scope.order = res;
//             })
//         }
//     });

//     $scope.submit = function () {
//         if ($scope.data.ean13 in $rootScope.ProductListByEan13){
//             $scope.errorMessage = "";
//             $state.go('select_quantity', {ean13: $scope.data.ean13});
//         }else{
//             $scope.errorMessage = $translate.instant("Unknown EAN13 Barcode");
//             angular.element(document.querySelector('#sound_user_error'))[0].play();
//         }
//     };

// }]);
