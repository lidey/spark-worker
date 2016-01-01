'use strict';

/* Controllers */

angular.module('app')
    .value('config', _system_info)
    .controller('AppCtrl', ['$scope', '$translate', '$localStorage', '$window', '$modal', '$http', 'config',
        function ($scope, $translate, $localStorage, $window, $modal, $http, config) {

            $scope.showMessage = function (message) {
                return $modal.open({
                    templateUrl: 'serverModalContent.html',
                    controller: 'ServerModalCtrl',
                    size: '',
                    resolve: {
                        message: function () {
                            return message;
                        }
                    }
                });
            };

            // add 'ie' classes to html
            var isIE = !!navigator.userAgent.match(/MSIE/i);
            isIE && angular.element($window.document.body).addClass('ie');
            isSmartDevice($window) && angular.element($window.document.body).addClass('smart');

            // config
            $scope.app = {
                name: config.name,
                hostname: config.hostname,
                port: config.port,
                company: config.company,
                version: config.version,
                // for chart colors
                color: {
                    primary: '#7266ba',
                    info: '#23b7e5',
                    success: '#27c24c',
                    warning: '#fad733',
                    danger: '#f05050',
                    light: '#e8eff0',
                    dark: '#3a3f51',
                    black: '#1c2b36'
                }
            };
            $http.get("user/current").then(function (resp) {
                $scope.user = resp.data.user;
                $scope.app.settings = resp.data.settings;
                $scope.$watch('app.settings', function () {
                    if ($scope.app.settings.asideDock && $scope.app.settings.asideFixed) {
                        // aside dock and fixed must set the header fixed.
                        $scope.app.settings.headerFixed = true;
                    }
                    $http.post("user/setting", $scope.app.settings);
                }, true);
            });


            // angular translate
            $scope.lang = {isopen: false};
            $scope.langs = {zh_CN: '中文', en: 'English', de_DE: 'German', it_IT: 'Italian'};
            $scope.selectLang = $scope.langs[$translate.proposedLanguage()] || "中文";
            $scope.setLang = function (langKey, $event) {
                // set the current lang
                $scope.selectLang = $scope.langs[langKey];
                // You can change the language during runtime
                $translate.use(langKey);
                $scope.lang.isopen = !$scope.lang.isopen;
            };

            function isSmartDevice($window) {
                // Adapted from http://www.detectmobilebrowsers.com
                var ua = $window['navigator']['userAgent'] || $window['navigator']['vendor'] || $window['opera'];
                // Checks for iOs, Android, Blackberry, Opera Mini, and Windows mobile devices
                return (/iPhone|iPod|iPad|Silk|Android|BlackBerry|Opera Mini|IEMobile/).test(ua);
            }

        }]);


app.controller('ServerModalCtrl', ['$scope', '$modalInstance', '$timeout', 'message', function ($scope, $modalInstance, $timeout, message) {
    $scope.message = message;

    $scope.cancel = function () {
        $modalInstance.close();
        //$modalInstance.dismiss('cancel');
    };

    $timeout(function () {
        $scope.cancel();
    }, 3 * 1000);
}]);