'use strict';


angular.module('mobile_app_purchase').factory(
        'ProductModel', [
        '$q', '$rootScope', 'jsonRpc',
        function ($q, $rootScope, jsonRpc) {

    return {
        LoadProduct: function() {
            return jsonRpc.call(
                    'mobile.app.purchase', 'get_products', []).then(function (res) {
                $rootScope.ProductListByEan13 = res;
                return res.length;
            });
        },

    };
}]);
