angular.module('app').run(
    [          '$rootScope', '$state', '$stateParams',
      function ($rootScope,   $state,   $stateParams) {
          $rootScope.$state = $state;
          $rootScope.$stateParams = $stateParams;
      }
    ]
  ).config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('app.job',{
                        url: '/job',
                        templateUrl: 'static/tpl/job/index.html',
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
                                                     'static/vendor/libs/moment.min.js']);
                                         })
                                }]
                  }
                    }).state('app.job.new',{
                         url: '/add',
                         templateUrl: 'static/tpl/job/job.new.html'
                    }).state('app.job.info', {
                         url: '/info/{id}',
                         templateUrl: 'static/tpl/job/job.info.html'
                    }).state('app.job.scriptAdd',{
                         url: '/script/add/{jobId}',
                         templateUrl: 'static/tpl/script/new.html'
                    }).state('app.job.list',{
                         url: '/script/list/{jobId}',
                         templateUrl: 'static/tpl/script/list.html'
                    }).state('app.job.scriptEdit',{
                         url: '/script/edit/{scriptId}',
                         templateUrl: 'static/tpl/script/info.html'
                    })


    }])