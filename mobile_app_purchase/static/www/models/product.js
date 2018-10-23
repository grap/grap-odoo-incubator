"use strict";
angular.module('mobile_app_purchase').factory(
        'ProductModel', [
        '$q', 'jsonRpc',
        function ($q, jsonRpc) {

    var product_promise = null;
    var products_by_barcode = {};

    return {
        reset_list: function() {
            products = {};
        },

        get_list: function(purchase_order) {
            product_promise = product_promise || jsonRpc.call(
                'mobile.app.purchase', 'get_products', 
                [{purchase_order: purchase_order}]).then(function (products) {
                    console.log(products);
                    products.forEach(function(product) {
                        products_by_barcode[product.barcode] = product;
                    });
                    return products_by_barcode;
            });
            return product_promise;
        },

        search_product: function(ean13) {
            return $q(function (success, error) {
                console.log(products_by_barcode);
                if (products_by_barcode[ean13]) {//search in cache
                    return success(products_by_barcode[ean13]);
                }
                jsonRpc.call('mobile.app.purchase', 'search_barcode', [{'barcode': ean13}]
                ).then(function (res) {
                    if (!res){
                        return $q.reject('Product not found');
                    } else {
                        products_by_barcode[ean13] = res; //set cache
                        return success(products_by_barcode[ean13]);
                    }
                });
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
