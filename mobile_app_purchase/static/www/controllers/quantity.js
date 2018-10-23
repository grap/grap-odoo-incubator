"use strict";
angular.module('mobile_app_purchase').controller(
        'QuantityCtrl',
        ['$scope', '$state', '$translate', 'PurchaseOrderModel', 'ProductModel',
        function ($scope, $state, $translate, PurchaseOrderModel, ProductModel,) {

    $scope.data = { };

    $scope.$on(
            '$stateChangeSuccess',
            function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'quantity') {
            console.log("FROMAGE");
            // Set Focus
            angular.element(document.querySelector('#input_quantity'))[0].focus();

            //Initialize default data
            $scope.errorMessage = '';
            $scope.data.qty = '';
            // Get Purchase order / Product Data
            PurchaseOrderModel.get_purchase_order(toParams.purchase_order_id).then(function (purchase_order) {
                console.log("purchase");
                console.log(purchase_order);
                $scope.purchase_order = purchase_order;
            });
            ProductModel.search_product(toParams.ean13).then(function (product) {
                console.log("product");
                console.log(product);
                $scope.product = product;
            });
        }
    });

    $scope.submit = function () {
        // Reset Focus, in case the quantity is not correct
        angular.element(document.querySelector('#input_quantity'))[0].focus();
        var parsed_qty = parseInt($scope.data.qty);
        if (! isNaN(parsed_qty)){
            if (parsed_qty < 1000000){
                PurchaseOrderModel.add_purchase_order_line(
                        $scope.purchase_order, $scope.product, parsed_qty).then(function (res){
                    angular.element(document.querySelector('#sound_ok'))[0].play();
                    $state.go('product', {purchase_order_id: $scope.purchase_order.id});
                    
                }, function(reason) {
                    $scope.errorMessage = $translate.instant("Something Wrong Happened");
                    angular.element(document.querySelector('#sound_error'))[0].play();
                });
            }else{
                $scope.errorMessage = $translate.instant("Too Big Quantity");
                angular.element(document.querySelector('#sound_error'))[0].play();
            }
        }
        else{
            $scope.errorMessage = $translate.instant("Incorrect Quantity");
            angular.element(document.querySelector('#sound_error'))[0].play();
        }
    };

    $scope.reset = function() {
        $state.go('product', {purchase_order_id: $scope.purchase_order.id});
    };

}]);










// 'use strict';


// angular.module('mobile_app_purchase').controller(
//         'SelectQuantityCtrl',
//         ['$scope', '$rootScope', 'jsonRpc', '$state', 'PurchaseOrderModel', '$translate',
//         function ($scope, $rootScope, jsonRpc, $state, PurchaseOrderModel, $translate) {

//     $scope.data = {
//         'qty': '',
//     };

//     $scope.$on(
//             '$stateChangeSuccess',
//             function(event, toState, toParams, fromState, fromParams){
//         if ($state.current.name === 'select_quantity') {
//             // Set Focus
//             angular.element(document.querySelector('#input_quantity'))[0].focus();

//             // Get Product Data
//             $scope.product = $rootScope.ProductListByEan13[toParams['ean13']];
//         }
//     });

//     $scope.submit = function () {
//         if ($scope.data.qty != null && !isNaN($scope.data.qty)){
//             if ($scope.data.qty < 1000000){
//                 if ($scope.data.qty > 0){
//                     PurchaseOrderModel.AddOrderLine(
//                             $rootScope.currentPurchaseOrderId, $scope.product.id,
//                             $scope.data.qty).then(function (res){
//                         angular.element(document.querySelector('#sound_quantity_selected'))[0].play();
//                         setTimeout(function(){
//                             $state.go('select_product');
//                         }, 300);
//                     }, function(reason) {
//                         $scope.errorMessage = $translate.instant("Something Wrong Happened");
//                     });
//                 }else{
//                     $scope.errorMessage = $translate.instant("Too Small Quantity");
//                     angular.element(document.querySelector('#sound_user_error'))[0].play();
//                 }
//             }else{
//                 $scope.errorMessage = $translate.instant("Too Big Quantity");
//                     angular.element(document.querySelector('#sound_user_error'))[0].play();
//             }
//         }
//         else{
//             $scope.errorMessage = $translate.instant("Incorrect Quantity");
//             angular.element(document.querySelector('#sound_user_error'))[0].play();
//         }
//     };

// }]);
