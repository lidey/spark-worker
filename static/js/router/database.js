'use strict';

/**
 * Config for the router
 */
angular.module('app')
    .config(
        ['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {
                $stateProvider
                // database
                    .state('database', {
                        abstract: true,
                        url: '/database',
                        templateUrl: 'static/tpl/database/database.html',
                        resolve: {
                            deps: ['$ocLazyLoad', 'uiLoad',
                                function ($ocLazyLoad, uiLoad) {
                                    return $ocLazyLoad.load(['angularBootstrapNavTree']).then(function () {
                                        return uiLoad.load(['static/js/app/database/database.js',
                                            'static/js/app/database/database-service.js',
                                            'static/vendor/libs/moment.min.js']);
                                    })
                                }]
                        }
                    })
                    .state('database.index', {
                        url: '/index',
                        templateUrl: 'static/tpl/database/database.index.html'
                    })
                    .state('database.add', {
                        url: '/add',
                        templateUrl: 'static/tpl/database/database.info.html',
                        resolve: {
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                    return $ocLazyLoad.load(['ui.select', 'textAngular']);
                                }]
                        }
                    })
                    .state('database.update', {
                        url: '/update/{uuid}',
                        templateUrl: 'static/tpl/database/database.info.html',
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