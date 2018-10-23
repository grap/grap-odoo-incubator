"use strict";
angular.module('mobile_app_purchase').factory(
        'ProductModel', [
        '$q', 'jsonRpc',
        function ($q, jsonRpc) {

    var product_promise = null;
    var products = {};

    return {
        reset_list: function() {
            products = {};
        },

        get_list: function(purchase_order) {
            product_promise = product_promise || jsonRpc.call(
                'mobile.app.purchase', 'get_products', 
                [{purchase_order: purchase_order}]).then(function (products) {
                    products.forEach(function(product) {
                        products[product.barcode] = product;
                        // products[product.barcode].found = true;
                    });
                    return products;
            });
            return product_promise;
        },

        search_product: function(ean13) {
            return $q(function (success, error) {
                if (products[ean13]) {//search in cache
                    return success(products[ean13]);
                }
                // jsonRpc.call('mobile.app.inventory', 'search_barcode', [{'barcode': ean13}]
                // ).then(function (res) {
                //     if (!res){
                //         res = {'found': false, 'name': 'unkown', 'barcode': ean13, 'custom_vals': {}}; //error('Product ' + ean13 + ' not found');
                //     } else {
                //         res.found = true;
                //     }
                //     products[ean13] = res; //set cache
                //     return success(products[ean13]);
                // });
            });
        },

        get_product: function(id) {
            var found = false;
            Object.values(products).some(function (product) {
                if (product.id == id)
                    return found = product;
            });
            return found;
        }    
    };
}]);
 



// 'use strict';


// angular.module('mobile_app_purchase').factory(
//         'ProductModel', [
//         '$q', '$rootScope', 'jsonRpc',
//         function ($q, $rootScope, jsonRpc) {

//     return {
//         LoadProduct: function() {
//             return jsonRpc.call(
//                     'mobile.app.purchase', 'get_products', []).then(function (res) {
//                 $rootScope.ProductListByEan13 = res;
//                 return res.length;
//             });
//         },

//     };
// }]);
