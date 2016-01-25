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
                            deps: ['$ocLazyLoad', 'uiLoad',
                                function ($ocLazyLoad, uiLoad) {
                                    return $ocLazyLoad.load(['angularBootstrapNavTree']).then(function () {
                                        return uiLoad.load(['static/js/app/server/server.js',
                                            'static/js/app/server/server-service.js',
                                            'static/js/app/spark/spark.js',
                                            'static/js/app/spark/spark-service.js',
                                            'static/vendor/libs/moment.min.js']);
                                    })

                                }]
                        }
                    })
                    .state('app.server.index', {
                        url: '/index',
                        views: {
                            '': {
                                templateUrl: 'static/tpl/server/server.index.html'
                            },
                            'aside': {
                                templateUrl: 'static/tpl/server/server.folder.tree.html'
                            }
                        }
                    })
                    .state('app.server.term', {
                        url: '/term',
                        views: {
                            '': {
                                templateUrl: 'static/tpl/server/server.term.html'
                            }
                        },
                        resolve: {
                            deps: ['$ocLazyLoad', 'uiLoad',
                                function ($ocLazyLoad, uiLoad) {
                                    return $ocLazyLoad.load(['ui.select']).then(function () {
                                        return uiLoad.load(['static/vendor/jquery/term/term.js',
                                            'static/js/app/server/term-directive.js']);
                                    });

                                }]
                        }
                    })
                    .state('app.server.file', {
                        url: '/file',
                        views: {
                            '': {
                                templateUrl: 'static/tpl/server/server.file.html'
                            }
                        }
                    });
            }
        ]
    );