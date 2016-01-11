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
                    .state('app.database', {
                        abstract: true,
                        url: '/database',
                        templateUrl: 'static/tpl/database/database.html',
                        resolve: {
                            deps: ['$ocLazyLoad', 'uiLoad',
                                function ($ocLazyLoad, uiLoad) {
                                    return $ocLazyLoad.load(['angularBootstrapNavTree']).then(function () {
                                        return uiLoad.load([
                                            'static/js/app/database/database.js',
                                            'static/js/app/database/database-service.js',
                                            'static/vendor/libs/moment.min.js']);
                                    })
                                }]
                        }
                    })
                    .state('app.database.index', {
                        url: '/index',
                        templateUrl: 'static/tpl/database/database.index.html'
                    })
                    //model
                    .state('app.model', {
                        abstract: true,
                        url: '/model',
                        templateUrl: 'static/tpl/database/model.html',
                        resolve: {
                            deps: ['$ocLazyLoad', 'uiLoad',
                                function ($ocLazyLoad, uiLoad) {
                                    return $ocLazyLoad.load(['angularBootstrapNavTree']).then(function () {
                                        return uiLoad.load([
                                            'static/js/app/database/model.js',
                                            'static/js/app/database/model-service.js',
                                            'static/js/app/database/database-service.js',
                                            'static/vendor/libs/moment.min.js']);
                                    })
                                }]
                        }
                    })
                    .state('app.model.index', {
                        url: '/index',
                        templateUrl: 'static/tpl/database/model.index.html'
                    });

            }
        ]
    );