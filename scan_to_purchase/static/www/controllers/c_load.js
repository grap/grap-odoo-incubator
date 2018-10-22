'use strict';


angular.module('scan_to_purchase').controller(
        'LoadCtrl', [
        '$scope', '$rootScope', 'jsonRpc', '$state', 'ProductProductModel', 'ResPartnerModel', 'PurchaseOrderModel', '$translate',
        function ($scope, $rootScope, jsonRpc, $state, ProductProductModel, ResPartnerModel, PurchaseOrderModel, $translate) {

    $scope.data = {}

    $scope.$on(
            '$stateChangeSuccess',
            function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'load') {
            $scope.data.product_ok = false;
            $scope.data.product_ko = false;
            $scope.data.supplier_ok = false;
            $scope.data.supplier_ko = false;
            $scope.data.order_ok = false;
            $scope.data.order_ko = false;

            $scope.loadingMessage = $translate.instant("Pending Loading ...");
            $scope.doneMessage = "";
            $scope.errorMessage = "";

            ProductProductModel.LoadProduct().then(function(product_qty){
                $scope.data.product_ok = true;
                ResPartnerModel.LoadSupplier().then(function(supplier_qty){
                    $scope.data.supplier_ok = true;
                    PurchaseOrderModel.LoadDraftOrder().then(function(order_qty){
                        $scope.data.order_ok = true;
                        $scope.doneMessage = $translate.instant("Loading Done");
                        setTimeout(function(){
                            $state.go('select_purchase_order');
                        }, 1500);
                    }, function(reason) {
                        $scope.LoadingError();
                    });
                }, function(reason) {
                    $scope.LoadingError();
                });
            }, function(reason) {
                $scope.LoadingError();
            });
        }
    });

    $scope.LoadingError = function () {
        $scope.loadingMessage = "";
        $scope.doneMessage = "";
        $scope.errorMessage = $translate.instant("Loading Failed");
        angular.element(document.querySelector('#sound_loading_failed'))[0].play();
    };

}]);
