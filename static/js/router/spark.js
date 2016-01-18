'use strict';

/**
 * Config for the router
 */
angular.module('app')
    .config(
        ['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {
                $stateProvider
                // spark
                    .state('app.spark', {
                        abstract: true,
                        url: '/spark',
                        templateUrl: 'static/tpl/spark/spark.html',
                        resolve: {
                            deps: ['uiLoad',
                                function (uiLoad) {
                                    return uiLoad.load(['static/js/app/spark/spark.js',
                                        'static/js/app/spark/spark-service.js',
                                        'static/vendor/libs/moment.min.js']);
                                }]
                        }
                    })
                    .state('app.spark.jobs', {
                        url: '/jobs',
                        templateUrl: 'static/tpl/spark/spark.job.list.html'
                    })
                    .state('app.spark.logs', {
                        url: '/logs',
                        views: {
                            '': {
                                templateUrl: 'static/tpl/spark/spark.job.log.list.html'
                            },
                            'aside': {
                                templateUrl: 'static/tpl/spark/spark.list.html'
                            }
                        }
                    })
                    .state('app.spark.add', {
                        url: '/add',
                        templateUrl: 'static/tpl/spark/spark.info.html',
                        resolve: {
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                    return $ocLazyLoad.load(['ui.select']);
                                }]
                        }
                    })
                    .state('app.spark.update', {
                        url: '/update/{uuid}',
                        templateUrl: 'static/tpl/spark/spark.info.html',
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