app.controller('ServerCtrl', ['$scope', 'serverService', '$stateParams', function ($scope, serverService, $stateParams) {

    $scope.refresh = function () {
        serverService.all().then(function (servers) {
            $scope.servers = servers;
            if ($scope.server == undefined)
                $scope.server = servers[0];
            else
                angular.forEach($scope.servers, function (server) {
                    if (server.uuid == $scope.server.uuid)
                        $scope.server = server;
                });
            $scope.server.selected = true;
            $scope.server.color = 'success';
            $scope.$broadcast('server', $scope.server);
        });
    };

    $scope.selectServer = function (server) {
        angular.forEach($scope.servers, function (server) {
            server.selected = false;
            $scope.server.color = 'info';
        });
        $scope.server = server;
        $scope.server.selected = true;
        $scope.server.color = 'success';
        $scope.$broadcast('server', $scope.server);
    };

    $scope.refresh();

}]);

app.controller('ServerDetailCtrl', ['$scope', 'serverService', '$stateParams', '$modal', function ($scope, serverService, $stateParams, $modal) {

    $scope.$on('server', function (event, data) {
        $scope.server = data;
        $scope.server.version = serverService.getVersion(data.version);
    });

    $scope.$on('message', function (event, data) {
        $scope.message = data;
    });

    $scope.delete = function (server) {
        $scope.showConfirm('请确认是否删除服务器:' + $scope.server.name).result.then(function (data) {
            if (data) {
                serverService.delete(server.uuid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.refresh();
                });
            }

        }, function () {
        });

    };

    $scope.testServer = function () {
        serverService.test($scope.server).then(function (message) {
            if (message.success) {
                $scope.showMessage(message)
            }
        });
    };

    $scope.open_term = function () {
        $modal.open({
            templateUrl: 'static/tpl/server/server.term.html',
            controller: 'ServerTermCtrl',
            size: '',
            resolve: {
                server: function () {
                    return $scope.server;
                },
                deps: ['uiLoad',
                    function (uiLoad) {
                        return uiLoad.load(['static/vendor/jquery/term/term.js',
                            'static/js/app/server/term-directive.js']);
                    }]
            }
        });
    };
}]);

app.controller('ServerEditCtrl', ['$scope', 'serverService', '$state', '$stateParams', function ($scope, serverService, $state, $stateParams) {
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
        serverService.save($scope.server).then(function (message) {
            $scope.showMessage(message).result.then(function () {
                $scope.refresh();
            }, function () {
            });
            $state.go('app.server.manager');
        });
    };

    $scope.testServer = function () {
        serverService.test($scope.server).then(function (message) {
            if (message.success) {
                $scope.server.success = !message.success;
                $scope.server.cpu = message.cpu;
                $scope.server.core = message.core;
                $scope.server.processor = message.processor;
                $scope.server.men = message.men;
            }
            $scope.showMessage(message)
        });
    };
}]);

app.controller('ServerTermCtrl', ['$scope', '$modalInstance', 'config', 'server', function ($scope, $modalInstance, config, server) {
    $scope.web_terminal_uri = 'ws://' + config.hostname + ':' + config.port + '/terminal?uuid=' + server.uuid;
    $scope.server = server;

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
}]);
