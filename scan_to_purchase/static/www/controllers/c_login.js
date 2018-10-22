'use strict';


angular.module('scan_to_purchase').controller(
        'LoginCtrl', [
        '$scope','$rootScope', 'jsonRpc', '$state', '$translate',
        function ($scope, $rootScope, jsonRpc, $state, $translate) {

    $scope.data = {
        'db': '',
        'db_list': [],
        'login': '',
        'password': '',
        'focus': true,
    };

    $scope.$on('$ionicView.beforeEnter', function() {
        if ($state.current.name === 'logout') {
            delete $rootScope.ProductListByEan13;
            delete $rootScope.OrderList;
            delete $rootScope.SupplierList;
            angular.element(document.querySelector('#sound_stop_session'))[0].play();
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
            $scope.errorMessage = $translate.instant("Unreachable Service");
        });
    };

    $scope.submit = function () {
        jsonRpc.login($scope.data.db, $scope.data.login, $scope.data.password).then(function (user) {
            jsonRpc.call('res.users', 'check_group', ['purchase.group_purchase_user']).then(function (res) {
                if (res){
                    angular.element(document.querySelector('#sound_start_session'))[0].play();
                    $scope.errorMessage = "";
                    $state.go('load');
                }
                else{
                    $scope.errorMessage = $translate.instant("Insufficient Acces Right: you should be member of 'Purchase / user' group.");
                }
            });
        }, function(e) {
            $scope.errorMessage = $translate.instant("Bad Login / Password");
        });
    };
}]);
