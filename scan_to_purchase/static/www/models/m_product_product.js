'use strict';


angular.module('scan_to_purchase').factory(
        'ProductProductModel', [
        '$q', '$rootScope', 'jsonRpc',
        function ($q, $rootScope, jsonRpc) {

    return {
        LoadProduct: function() {
            console.log("coincoin");
            return jsonRpc.call(
                    'product.product', 'scan_to_purchase_load_product', []).then(function (res) {
                console.log(res);
                $rootScope.ProductListByEan13 = res;
//                angular.forEach(res, function(product) {
//                    $rootScope.ProductListByEan13[product['ean13']] = product;
//                });
                return res.length;
            });
        },

    };
}]);
