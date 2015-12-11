angular.module('app') .config(
        ['$stateProvider', '$urlRouterProvider',
            function ($stateProvider) {

                  $stateProvider
                    .state('scheduler', {
                        url: '/scheduler',
                        templateUrl: 'static/tpl/scheduler/index.html',
                        resolve:{
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                     return $ocLazyLoad.load('textAngular').then(function(){
                                    return $ocLazyLoad.load(['static/js/app/scheduler/scheduler.js',
                                                   'static/js/app/scheduler/scheduler-service.js',
                                                     'static/vendor/libs/moment.min.js']);
                                         })
                                }]
                        }
                    }).state('scheduler.manager', {
                        url: '/manager',
                        templateUrl: 'static/tpl/scheduler/scheduler.info.html'
                    })
                    .state('scheduler.add', {
                        url: '/add',
                        templateUrl: 'static/tpl/scheduler/scheduler.html',
                        resolve: {
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                    return $ocLazyLoad.load(['ui.select', 'textAngular']);
                                }]
                        }
                    })
                    .state('scheduler.update', {
                        url: '/update/{uuid}',
                        templateUrl: 'static/tpl/scheduler/scheduler.html',
                        resolve: {
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                    return $ocLazyLoad.load(['ui.select', 'textAngular']);
                                }]
                        }
                    });

            }

        ])
