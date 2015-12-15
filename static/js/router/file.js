angular.module('app').run(
    [          '$rootScope', '$state', '$stateParams',
      function ($rootScope,   $state,   $stateParams) {
          $rootScope.$state = $state;
          $rootScope.$stateParams = $stateParams;
      }
    ]
  ).config(['$stateProvider', function ($stateProvider) {
        $stateProvider.state('app.file',{
                        url: '/file',
                        templateUrl: 'static/tpl/file/upload.html',
                        resolve: {
                                  deps: ['$ocLazyLoad',
                                    function( $ocLazyLoad){
                                      return $ocLazyLoad.load('angularFileUpload').then(
                                          function(){
                                             return $ocLazyLoad.load('static/js/app/file/file-upload.js');
                                          }
                                      );
                                  }]
                              }
                    })


    }])