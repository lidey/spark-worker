'use strict';

/**
 * Config for the router
 */
angular.module('app')
    .run(
        ['$rootScope', '$state', '$stateParams',
            function ($rootScope, $state, $stateParams) {
                $rootScope.$state = $state;
                $rootScope.$stateParams = $stateParams;
            }
        ]
    )
    .config(
        ['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {

                $urlRouterProvider
                    .otherwise('/app/index');
                $stateProvider
                    .state('app', {
                        abstract: true,
                        url: '/app',
                        templateUrl: 'static/tpl/app.html'
                    })
                    .state('app.index', {
                        url: '/index',
                        templateUrl: 'static/tpl/app_index.html',
                        resolve: {
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                    return $ocLazyLoad.load(['static/js/controllers/app-index.js']);
                                }]
                        }
                    }).state('app.docs', {
                    url: '/docs',
                    templateUrl: 'static/tpl/docs.html'
                    })

            }
        ]
    );