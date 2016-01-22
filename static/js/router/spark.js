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
                        views: {
                            '': {
                                templateUrl: 'static/tpl/spark/spark.job.list.html'
                            },
                            'aside': {
                                templateUrl: 'static/tpl/spark/spark.list.html'
                            }
                        }
                    })
                    .state('app.spark.running', {
                        url: '/running',
                        views: {
                            '': {
                                templateUrl: 'static/tpl/spark/spark.job.running.list.html'
                            }
                        }
                    })
                    .state('app.spark.logs', {
                        url: '/logs',
                        views: {
                            '': {
                                templateUrl: 'static/tpl/spark/spark.job.log.list.html'
                            }
                        }
                    });
            }
        ]
    );