app.controller('ServerCtrl', ['$scope', 'serverService', '$stateParams', function ($scope, serverService, $stateParams) {

    $scope.refresh = function () {
        serverService.all().then(function (servers) {
            $scope.servers = servers;
            if ($scope.server == undefined)
                $scope.server = servers[0];
            else
                angular.forEach($scope.servers, function (server) {
                    if (server.uuid == $scope.server.uuid)
                        server.selected = true;
                });
            $scope.server.selected = true;
            $scope.$broadcast('server', $scope.server);
        });
    };

    $scope.selectServer = function (server) {
        angular.forEach($scope.servers, function (server) {
            server.selected = false;
        });
        $scope.server = server;
        $scope.server.selected = true;
        $scope.$broadcast('server', $scope.server);
    };


    $scope.refresh();

}]);

app.controller('ServerDetailCtrl', ['$scope', 'serverService', '$stateParams', function ($scope, serverService, $stateParams) {

    $scope.$on('server', function (event, data) {
        $scope.server = data;
        $scope.server.version = serverService.getVersion(data.version);
    });

    $scope.$on('message', function (event, data) {
        $scope.message = data;
    });

    $scope.delete = function (server) {
        console.log(server);
        serverService.delete(server.uuid).then(function (message) {
            $scope.showMessage(message)
        });
    }
}]);

app.controller('ServerEditCtrl', ['$scope', 'serverService', '$state', '$stateParams', function ($scope, serverService, $state, $stateParams) {
    console.log($scope.server);
    if ($stateParams.uuid != null) {
        serverService.get($stateParams.uuid).then(function (data) {
            $scope.server = data;
            $scope.server.success = true;
            $scope.server.version = serverService.getVersion(data.version);
        });
        $scope.$on('server', function (event, data) {
            $scope.server = data;
            $scope.server.success = true;
            $scope.server.version = serverService.getVersion(data.version);
        });
    } else {
        $scope.server = {};
        $scope.server.success = true;
    }
    $scope.versions = serverService.getVersionArrayAll();
    $scope.saveServer = function () {
        console.log($scope.server);
        serverService.save($scope.server).then(function (message) {
            $scope.showMessage(message)
            $state.go('server.manager');
        });
    };

    $scope.testServer = function () {
        serverService.test($scope.server).then(function (message) {
            if (message.success) {
                $scope.server.success = !message.success;
                $scope.server.cpu = message.cpu;
                $scope.server.core = message.core;
                $scope.server.men = message.men;
                console.log(message);
            }
            $scope.showMessage(message)
        });
    };
}]);
