// Copyright (C) 2015-Today GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
//  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

"use strict";

angular.module('mobile_app_purchase').factory(
        'PartnerModel', [
        '$q', 'jsonRpc',
        function ($q, jsonRpc) {

    function reset() {
        data.partner_promise = null;
        data.partners = [];
    }
    var data = {}
    reset();

    return {
        get_list: function() {
            //get partners
            //return a promise
            data.partner_promise = data.partner_promise || jsonRpc.call(
                'mobile.app.purchase', 'get_partners', [{}]
                ).then(function (partners) {
                    data.partners = partners;
                    return partners;
                }
            );
            return data.partner_promise;
        },

    };
}]);
