'use strict';


angular.module('scan_to_purchase').factory(
        'ResPartnerModel', [
        '$q', '$rootScope', 'jsonRpc',
        function ($q, $rootScope, jsonRpc) {

    return {
        LoadSupplier: function() {
            return jsonRpc.searchRead(
                    'res.partner', [['supplier', '=', '1']], [
                    'id', 'name', 'city', 'country_id', 'purchase_order_count',
                    ]).then(function (res) {
                $rootScope.SupplierList = res.records;
                return res.records.length;
            });
        },

    };
}]);
