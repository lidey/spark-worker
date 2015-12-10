app.controller('ServerCtrl', ['$scope', 'serverService', '$stateParams', '$modal', function ($scope, serverService, $stateParams, $modal) {

    $scope.alerts = [];

    $scope.refresh = function () {
        serverService.all().then(function (servers) {
            $scope.servers = servers;
            var uuid = null;
            if ($scope.server != undefined)
                uuid = $scope.server.uuid;
            else
                uuid = servers[servers.length - 1].uuid;
            $scope.server = servers[servers.length - 1];
            angular.forEach($scope.servers, function (server) {
                if (server.uuid == uuid) {
                    $scope.server = server;
                }
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

    $scope.$on('message', function (event, data) {
        $scope.alerts.push({type: data.success ? 'success' : 'danger', msg: data.content});
        $scope.refresh();
    });

    $scope.showMessage = function (message) {
        $modal.open({
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

    $scope.refresh();

}]);

app.controller('ServerDetailCtrl', ['$scope', 'serverService', '$stateParams', '$modal', function ($scope, serverService, $stateParams, $modal) {
    $scope.$on('server', function (event, data) {
        serverService.get(data.uuid).then(function (data) {
            $scope.server = data;
            $scope.server.success = true;
            $scope.server.version = serverService.getVersion(data.version);
        });
    });

    $scope.delete = function (server) {
        $modal.open({
            templateUrl: 'serverConfirmContent.html',
            controller: 'ServerConfirmCtrl',
            size: '',
            resolve: {
                server: function () {
                    return server;
                }
            }
        }).result.then(function (server) {
            serverService.delete(server.uuid).then(function (message) {
                $scope.showMessage(message);
                if (message.success)
                    $scope.refresh();
            });
        }, function () {
        });
    }
}]);

app.controller('ServerEditCtrl', ['$scope', 'serverService', '$state', '$stateParams', function ($scope, serverService, $state, $stateParams) {

    $scope.versions = serverService.getVersionArrayAll();

    if ($stateParams.uuid != null) {
        serverService.get($stateParams.uuid).then(function (data) {
            $scope.server = data;
            $scope.server.success = false;
            $scope.server.version = serverService.getVersion(data.version);
        });
        $scope.$on('server', function (event, data) {
            serverService.get(data.uuid).then(function (data) {
                $scope.server = data;
                $scope.server.success = false;
                $scope.server.version = serverService.getVersion(data.version);
            });
        });
    } else {
        $scope.server = {};
        $scope.server.success = false;
    }


    $scope.saveServer = function () {
        serverService.save($scope.server).then(function (message) {
            $scope.showMessage(message);
            if (message.success) {
                $scope.refresh();
                $scope.selectServer(message.server);
                $state.go('server.manager');
            }
        });
    };

    $scope.testServer = function () {
        serverService.test($scope.server).then(function (message) {
            if (message.success) {
                $scope.server.success = message.success;
                $scope.server.cpu = message.cpu;
                $scope.server.core = message.core;
                $scope.server.processor = message.processor;
                $scope.server.men = message.men;
            }
            $scope.showMessage(message)
        });
    };
}]);

app.controller('ServerModalCtrl', ['$scope', '$modalInstance', 'message', function ($scope, $modalInstance, message) {
    $scope.message = message;

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);


app.controller('ServerConfirmCtrl', ['$scope', '$modalInstance', 'server', 'serverService', function ($scope, $modalInstance, server, serverService) {
    $scope.server = server;
    $scope.message = {success: true, content: '请确认是否删除服务器.'};
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.ok = function () {
        $modalInstance.close(server);
    }
}]);