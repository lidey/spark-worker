'use strict';

/* Controllers */

app
// Flot Chart controller
    .controller('IndexCtrl', ['$scope', '$http', '$sce', function ($scope, $http, $sce) {
        $scope.saveAny = function () {
            $http.get('job/start').then(function (resp) {
                $scope.out = $sce.trustAsHtml(resp.data.log);
                $scope.user = resp.data.user;
            });
        }


    }]);