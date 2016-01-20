'use strict';

/**
 * Config for the router
 */
angular.module('app').config(
    ['$stateProvider', '$urlRouterProvider',
        function ($stateProvider) {
            $stateProvider
                .state('app.scheduler', {
                    abstract: true,
                    url: '/scheduler',
                    templateUrl: 'static/tpl/scheduler/scheduler.html',
                    resolve: {
                        deps: ['uiLoad',
                            function (uiLoad) {
                                return uiLoad.load([
                                    'static/js/app/scheduler/scheduler.js',
                                    'static/js/app/scheduler/scheduler-service.js',
                                    'static/js/app/job/job-service.js',
                                    'static/js/app/spark/spark-service.js',
                                    'static/vendor/libs/moment.min.js']);
                            }]
                    }
                })
                .state('app.scheduler.list', {
                    url: '/list',
                    templateUrl: 'static/tpl/scheduler/scheduler.list.html'
                })
                .state('app.scheduler.log', {
                    url: '/log',
                    templateUrl: 'static/tpl/scheduler/scheduler.log.list.html'
                });

        }

    ])
