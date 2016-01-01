'use strict';

/**
 * Config for the router
 */
angular.module('app')
    .config(
        ['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {
                $stateProvider
                // server
                    .state('app.server', {
                        abstract: true,
                        url: '/server',
                        templateUrl: 'static/tpl/server/server.html',
                        resolve: {
                            deps: ['uiLoad',
                                function (uiLoad) {
                                    return uiLoad.load(['static/js/app/server/server.js',
                                        'static/js/app/server/server-service.js',
                                        'static/vendor/libs/moment.min.js']);
                                }]
                        }
                    })
                    .state('app.server.manager', {
                        url: '/manager',
                        templateUrl: 'static/tpl/server/server.detail.html'
                    })
                    .state('app.server.add', {
                        url: '/add',
                        templateUrl: 'static/tpl/server/server.info.html',
                        resolve: {
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                    return $ocLazyLoad.load(['ui.select', 'textAngular']);
                                }]
                        }
                    })
                    .state('app.server.update', {
                        url: '/update/{uuid}',
                        templateUrl: 'static/tpl/server/server.info.html',
                        resolve: {
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                    return $ocLazyLoad.load(['ui.select', 'textAngular']);
                                }]
                        }
                    });
            }
        ]
    );