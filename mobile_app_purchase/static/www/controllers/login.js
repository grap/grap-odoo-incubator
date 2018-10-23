// Copyright (C) 2015-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
//  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"use strict";

angular.module('mobile_app_purchase').controller(
        'LoginCtrl', [
        '$scope', '$rootScope', 'jsonRpc', '$state', '$translate', 'ProductModel',
        function ($scope, $rootScope, jsonRpc, $state, $translate, ProductModel) {

    $scope.data = {
        'db': '',
        'db_list': [],
        'login': '',
        'password': '',
    };

    $scope.$on('$ionicView.beforeEnter', function() {
        if ($state.current.name === 'logout') {
            ProductModel.reset_list();
            jsonRpc.logout(true);
        }
    });

    $scope.init = function () {
        // Set focus
        angular.element(document.querySelector('#input_login'))[0].focus();

        // Load available databases
        jsonRpc.get_database_list().then(function(db_list){
            $scope.data.db_list = db_list;
            if (db_list.length >= 1) {
                $scope.data.db = db_list[0];
            }
        }, function(reason) {
            angular.element(document.querySelector('#sound_error'))[0].play();
            $rootScope.errorMessage = $translate.instant("Unreachable Service");
        });
    };

    $scope.submit = function () {
        jsonRpc.login($scope.data.db, $scope.data.login, $scope.data.password).then(function (user) {
            jsonRpc.call('mobile.app.purchase', 'check_group', ['purchase.group_purchase_user']).then(function (res) {
                if (res){
                    $rootScope.errorMessage = "";
                    $state.go('purchase_order');
                }
                else{
                    angular.element(document.querySelector('#sound_error'))[0].play();
                    $rootScope.errorMessage = $translate.instant("Insufficient Acces Right: you should be member of 'Purchase / user' group.");
                }
            });
        }, function(reason) {
            angular.element(document.querySelector('#sound_error'))[0].play();
            $rootScope.errorMessage = $translate.instant("Bad Login / Password");
        });
    };
}]);
