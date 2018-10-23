// Copyright (C) 2015-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
//  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"use strict";

angular.module('mobile_app_purchase').controller(
    'PurchaseOrderCtrl', [
    '$scope', '$rootScope', '$state', '$translate', 'PurchaseOrderModel', 'ProductModel', ,
    function ($scope, $rootScope, $state, $translate, PurchaseOrderModel, ProductModel) {

    $scope.data = {
        'purchase_order_list': [],
        'purchase_order_filter': null,
    };

    $scope.$on(
        '$stateChangeSuccess',
        function(event, toState, toParams, fromState, fromParams){
        if ($state.current.name === 'purchase_order') {
            $scope.data.purchase_order_filter = null;
            PurchaseOrderModel.get_list().then(function (purchase_order_list) {
                $scope.data.purchase_order_list = purchase_order_list;
            }, function(reason) {
                angular.element(document.querySelector('#sound_error'))[0].play();
                $rootScope.errorMessage = $translate.instant("Loading purchase orders failed");
            });
        }
    });

    $scope.create_purchase_order = function () {
        $state.go('partner');
    };

    $scope.select_purchase_order = function (purchase_order) {
        // Load Products
        ProductModel.get_list(purchase_order).then(function(product_list) {
            $state.go('product', {purchase_order_id: purchase_order.id});
        }, function(reason) {
            angular.element(document.querySelector('#sound_error'))[0].play();
                $rootScope.errorMessage = $translate.instant("Loading products failed");
        });

    };
}]);
