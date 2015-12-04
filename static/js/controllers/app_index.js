'use strict';

/* Controllers */

app
// Flot Chart controller
    .controller('IndexCtrl', ['$scope', '$http', '$sce', '$stateParams', function ($scope, $http, $sce, $stateParams) {
        console.log($stateParams);
        $scope.saveAny = function () {
            $http.post('job/start', $scope.user).then(function (resp) {
                $scope.out = $sce.trustAsHtml(resp.data.log);
                $scope.user = resp.data.user;
            });
        }


    }]);