angular.module('app').run(
    [          '$rootScope', '$state', '$stateParams',
      function ($rootScope,   $state,   $stateParams) {
          $rootScope.$state = $state;
          $rootScope.$stateParams = $stateParams;
      }
    ]
  ).config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('app.job.script',{
                       abstract:true,
                        url: '/script',
                        templateUrl: 'static/tpl/script/list.html'
                    })


    }])