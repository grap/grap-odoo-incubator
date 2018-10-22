// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'mobile_app_purchase' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module(
        'mobile_app_purchase', [
        'ionic', 'ui.router', 'odoo', 'pascalprecht.translate'])

.run(function($ionicPlatform) {
    $ionicPlatform.ready(function() {
        // Hide the accessory bar by default (remove this to show the 
        //accessory bar above the keyboard for form inputs)
        if(window.StatusBar) {
            StatusBar.styleDefault();
        }
    });
})
.run(['jsonRpc', '$state', '$rootScope', function (jsonRpc, $state, $rootScope) {
    jsonRpc.errorInterceptors.push(function (a) {
        if (a.title === 'session_expired')
            $state.go('login');
    });
    $rootScope.logout = function() {
        $state.go('logout');
    };
}])
.config([
        '$ionicConfigProvider', '$stateProvider', '$urlRouterProvider', '$translateProvider',
        function ($ionicConfigProvider, $stateProvider, $urlRouterProvider, $translateProvider) {

    $stateProvider.state(
        'login', {
            url: '/login',
            templateUrl: 'views/login.html',
            controller: 'LoginCtrl'
    }).state(
        'logout', {
            url: '/logout',
            templateUrl: 'views/login.html',
            controller: 'LoginCtrl'
    }).state(
        'credit', {
            url: '/credit',
            templateUrl: 'views/credit.html',
            controller: 'CreditCtrl'
    }).state(
        'purchase_order', {
            url: '/purchase_order',
            templateUrl: 'views/purchase_order.html',
            controller: 'PurchaseOrderCtrl'
    }).state(
        'partner', {
            url: '/partner',
            templateUrl: 'views/partner.html',
            controller: 'PartnerCtrl'
    }).state(
        'product', {
            url: '/purchase_order/{purchase_order_id:int}/product',
            templateUrl: 'views/product.html',
            controller: 'ProductCtrl'
    }).state(
        'quantity', {
            url: '/purchase_order/{purchase_order_id:int}/product/:ean13',
            templateUrl: 'views/quantity.html',
            controller: 'QuantityCtrl'
    });

    $ionicConfigProvider.views.transition('none');

    $urlRouterProvider.otherwise('login');

    $translateProvider.useStaticFilesLoader({
        prefix: 'i18n/',
        suffix: '.json'
    }).registerAvailableLanguageKeys(['en', 'fr'], {
        'en' : 'en', 'en_GB': 'en', 'en_US': 'en',
        'fr' : 'fr',
    })
    .preferredLanguage('en')
    .fallbackLanguage('en')
    .determinePreferredLanguage()
    .useSanitizeValueStrategy('escapeParameters');
}])
.controller('AppCtrl', [
    '$scope', '$state', '$stateParams', '$rootScope',
    function($scope, $state, $stateParams, $rootScope) {
        $rootScope.$on("$stateChangeError", console.log.bind(console));
        $scope.$on('$stateChangeSuccess',
            function(evt, toState, toParams, fromState, fromParams) {
                //for side menu
                $rootScope.currentState = toState.name;
                $rootScope.params = toParams;
            }
        );
    }
])

;
