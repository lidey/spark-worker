app.controller('ServerCtrl', ['$scope', 'serverService', '$stateParams', function ($scope, serverService, $stateParams) {

    $scope.refresh = function (uuid) {
        serverService.all().then(function (servers) {
            $scope.servers = servers;
            if (uuid != undefined) {
                $scope.selectServer({uuid: uuid});
            }
        });
        if (uuid == undefined) {
            $scope.$broadcast('server', undefined);
        }
    };

    $scope.selectServer = function (server) {
        angular.forEach($scope.servers, function (tmp) {
            if (tmp.uuid == server.uuid) {
                tmp.selected = true;
                tmp.color = 'success';
                $scope.server = tmp;
                $scope.$broadcast('server', tmp);
            } else {
                tmp.selected = false;
                tmp.color = 'info';
            }

        });
    };
    $scope.refresh();

}]);

app.controller('ServerDetailCtrl', ['$scope', 'serverService', '$stateParams', '$modal', function ($scope, serverService, $stateParams, $modal) {

    $scope.$on('server', function (event, data) {

        serverService.get(data.uuid).then(function (data) {
            $scope.server = data;
            $scope.server.version = serverService.getVersion(data.version);
        });
        if (data != undefined)
            $scope.server.version = serverService.getVersion(data.version);
    });

    $scope.$on('message', function (event, data) {
        $scope.message = data;
    });

    $scope.delete = function (server) {
        $scope.showConfirm('请确认是否删除服务器:' + $scope.server.title).result.then(function (data) {
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
                $scope.refresh(message.uuid);
            }, function () {
            });
            $state.go('app.server.index');
        });
    };

    $scope.testServer = function () {
        serverService.test($scope.server).then(function (message) {
            if (message.success) {
                $scope.server.success = !message.success;
                $scope.server.processor = message.processor;
                $scope.server.memory = message.memory;
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
