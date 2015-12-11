angular.module('app').run(
    [          '$rootScope', '$state', '$stateParams',
      function ($rootScope,   $state,   $stateParams) {
          $rootScope.$state = $state;
          $rootScope.$stateParams = $stateParams;
      }
    ]
  ).config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('app.process',{
                        url: '/process',
                        templateUrl: 'static/tpl/process/index.html',
                        resolve: {
                            deps: ['$ocLazyLoad',
                                function ($ocLazyLoad) {
                                     return $ocLazyLoad.load('textAngular').then(function(){
                                    return $ocLazyLoad.load(['static/js/app/job/job.js',
                                                   'static/js/app/job/job-service.js',
                                                        'static/js/app/data_service.js',
                                                         'static/js/app/script/script.js',
                                                   'static/js/app/script/script-service.js',
                                                   'static/js/app/data_service.js',
                                                  'static/js/app/process/process.js',
                                                  'static/js/app/process/process-service.js',
                                                     'static/vendor/libs/moment.min.js']);
                                         })
                                }]
                  }
                    }).state('app.process.manager',{
                         url: '/manager',
                         templateUrl: 'static/tpl/process/index.html'
                    })


    }])