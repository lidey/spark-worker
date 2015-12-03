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
                                                     'static/vendor/libs/moment.min.js']);
                                         })
                                }]
                  }
                    }).state('app.job.new',{
                         url: '/add',
                         templateUrl: 'static/tpl/job/job.new.html'
                    }).state('app.job.list',{
                         url: '/list/{status:[0-9]{1,5}}',
                         templateUrl: 'static/tpl/job/job.list.html'
                    }).state('app.job.info', {
                         url: '/info/{id}',
                         templateUrl: 'static/tpl/job/job.info.html'
                    })


    }])