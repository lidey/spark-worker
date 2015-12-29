'use strict';

/* Controllers */

angular.module('app')
    .value('config', {
        name: '大数据云--数据调度系统',
        hostname: '127.0.0.1',
        port: '8880',
        company: '软通动力信息技术（集团）有限公司',
        version: '0.0.1',
    })
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
            $http.get("user/current").then(function (resp) {
                $scope.user = resp.data;
            });
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
                },
                settings: {
                    themeID: 1,
                    navbarHeaderColor: 'bg-black',
                    navbarCollapseColor: 'bg-white-only',
                    asideColor: 'bg-black',
                    headerFixed: true,
                    asideFixed: false,
                    asideFolded: false,
                    asideDock: false,
                    container: false
                }
            };

            // save settings to local storage
            if (angular.isDefined($localStorage.settings)) {
                $scope.app.settings = $localStorage.settings;
            } else {
                $localStorage.settings = $scope.app.settings;
            }
            $scope.$watch('app.settings', function () {
                if ($scope.app.settings.asideDock && $scope.app.settings.asideFixed) {
                    // aside dock and fixed must set the header fixed.
                    $scope.app.settings.headerFixed = true;
                }
                // save to local storage
                $localStorage.settings = $scope.app.settings;
            }, true);

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
    if (message.success) {
        $timeout(function () {
            $scope.cancel();
        }, 3 * 1000);
    } else {
        $scope.theme = "text-danger"
    }
}]);