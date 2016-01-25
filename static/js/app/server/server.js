app.controller('ServerCtrl', ['$scope', 'serverService', '$timeout', '$modal', function ($scope, serverService, $timeout, $modal) {

    var tree;
    $scope.folder_data = [];
    $scope.folder_tree = tree = {};
    $scope.reload = function () {
        $scope.folder_data = [];
        var data_root = {
            uid: 'root-node',
            type: 'root',
            label: '目录管理',
            icon: 'fa fa-folder-o',
            data: {title: '目录管理'}
        };
        serverService.tree().then(function (data) {
            data_root.children = data;
            $scope.folder_data.push(data_root);
        });
        $scope.doing_async = true;
        $timeout(function () {
            $scope.doing_async = false;
            tree.expand_all();
            if ($scope.branch != undefined)
                if (tree.select_branch_uid($scope.branch.uid) == null)
                    $scope.$broadcast('branch', null);
        }, 1000);
    };
    $scope.folder_tree_handler = function (branch) {
        if (branch.type != null) {
            $scope.branch = branch;
            $scope.folder = branch.data;
            $scope.$broadcast('folder', branch.data);
        }
    };

    $scope.add_folder = function () {
        $scope.edit_folder({});
    };

    $scope.edit_folder = function (folder) {
        $modal.open({
            templateUrl: 'static/tpl/server/server.folder.info.html',
            controller: 'ServerEditCtrl',
            size: 'lg',
            resolve: {
                server: function () {
                    return null;
                },
                folder: function () {
                    return folder;
                }
            }
        }).result.then(function (message) {
            if (message.success) {
                $scope.showMessage(message);
                $scope.reload();
            }
        });
    };

    $scope.delete_folder = function (folder) {
        $scope.showConfirm('<p>请确认是否是要删除目录:' + folder.title + '?</p>').result.then(function (data) {
            if (data) {
                serverService.folder_delete(folder.uuid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.reload();
                });
            }
        });
    };

}]);

app.controller('ServerIndexCtrl', ['$scope', 'serverService', '$modal', '$compile', function ($scope, serverService, $modal, $compile) {

    $scope.$on('message', function (event, data) {
        $scope.message = data;
    });

    $scope.grid = {};
    $scope.$on('folder', function (event, data) {
        $scope.folder = data;
        if (data.uuid != undefined) {
            var url = 'server/list?f_uuid=' + data.uuid;
            if ($scope.grid.servers == undefined) {
                $scope.dt_option = {
                    'language': {
                        'url': 'static/vendor/jquery/datatables/i18n/zh_CN.json'

                    },
                    ajax: {
                        url: url,
                        dataSrc: 'servers'
                    },
                    columns: [
                        {title: '主键', data: 'uuid', visible: false},
                        {title: '名称', data: 'title', width: '30%'},
                        {title: '服务器地址', data: 'host', width: '12%'},
                        {title: '账号', data: 'name', width: '8%', visible: false},
                        {title: '类型', data: 'type', width: '10%'},
                        {title: '创建时间', data: 'created_time', width: '10%'}
                    ],
                    columnDefs: [
                        {
                            targets: [1],
                            render: function (data, type, row) {
                                return '<a ng-click="edit_server(\'' + row.uuid + '\')" class="text-info"><i class="fa icon-ghost m-r-xs"></i>' + data + '</a>';
                            }
                        },
                        {
                            targets: [5],
                            render: function (data, type, row) {
                                return new Date(parseInt(data)).toLocaleString().substr(0, 10);
                            }
                        },
                        {
                            title: '操作', width: '25%', targets: [6], data: 'uuid', orderable: false,
                            render: function (data, type, row) {
                                var option = '';
                                option += '<a ng-click="test_server(\'' + data + '\')" class="text-info m-r-md"><i class="fa  fa-play m-r-xs"></i>测试</a>';
                                if (row.type == 'Spark')
                                    option += '<a ng-click="allocation_server(\'' + data + '\')" class="text-info m-r-md"><i class="fa fa-sliders m-r-xs"></i>配置</a>';
                                option += '<a ng-click="delete_server(\'' + data + '\',\'' + row.title + '\')" class="text-warning"><i class="fa fa-times m-r-xs"></i>删除</a>';
                                return option;
                            }
                        }
                    ],
                    "fnCreatedRow": function (nRow, aData, iDataIndex) {
                        $compile(nRow)($scope);
                    }
                };
            } else {
                $scope.jobGrid.jobs.api().ajax.url(url).load();
            }
        }
    });
    $scope.add_server = function (f_uuid) {
        $scope.edit_server(undefined, f_uuid);
    };

    $scope.edit_server = function (uuid, f_uuid) {
        $modal.open({
            templateUrl: 'static/tpl/server/server.info.html',
            controller: 'ServerEditCtrl',
            size: 'lg',
            resolve: {
                folder: function () {
                    return null;
                },
                server: function () {
                    return {uuid: uuid, f_uuid: f_uuid};
                },
                deps: ['$ocLazyLoad',
                    function ($ocLazyLoad) {
                        return $ocLazyLoad.load(['ui.select']);
                    }]
            }
        }).result.then(function (message) {
            $scope.showMessage(message);
            if (message.success) {
                $scope.grid.servers.api().ajax.reload();
            }
        });
    };

    $scope.allocation_server = function (s_uuid) {
        $modal.open({
            templateUrl: 'static/tpl/spark/spark.info.html',
            controller: 'SparkEditCtrl',
            size: 'lg',
            resolve: {
                spark: function () {
                    return {s_uuid: s_uuid};
                },
                deps: ['uiLoad',
                    function (uiLoad) {
                        return uiLoad.load(['static/js/app/server/server.js',
                            'static/js/app/server/server-service.js']);
                    }]
            }
        }).result.then(function (message) {
            $scope.showMessage(message);
        });
    };

    $scope.delete_server = function (uuid, title) {
        $scope.showConfirm('<p>请确认是否是要删除服务器连接:' + title + '?</p>').result.then(function (data) {
            if (data) {
                serverService.delete(uuid).then(function (message) {
                    $scope.showMessage(message);
                    if (message.success) {
                        $scope.grid.servers.api().ajax.reload();
                    }
                });
            }
        });
    };

    $scope.test_server = function (uuid) {
        serverService.test(uuid).then(function (message) {
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

app.controller('ServerEditCtrl', ['$scope', 'serverService', '$modalInstance', 'folder', 'server', function ($scope, serverService, $modalInstance, folder, server) {

    $scope.alerts = [];

    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    if (server != null) {
        $scope.server = server;
        $scope.versions = serverService.getVersionArrayAll();
        if (server.uuid != undefined) {
            serverService.get(server.uuid).then(function (data) {
                $scope.server = data;
                $scope.server.version = serverService.getVersion(data.version);
            });
        }

    }

    if (folder != null) {
        $scope.folder = folder;
        if (folder.uuid != undefined) {
            serverService.folder_get(folder.uuid).then(function (data) {
                $scope.folder = data;
            });
        }
    }

    $scope.save_folder = function () {
        serverService.folder_save($scope.folder).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

    $scope.variables = {};
    $scope.variable = {};
    $scope.add_variable = function (variable) {
        if (variable.key.length > 0 && variable.key.length > 0) {
            $scope.variables[variable.key] = variable.value;
            $scope.variable = {};
        }
    };

    $scope.edit_variable = function (key) {
        $scope.variable.key = key;
        $scope.variable.value = $scope.variables[key];
    };

    $scope.remove_variable = function (key) {
        delete $scope.variables[key];
    };

    $scope.save_server = function () {
        serverService.save($scope.server).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };
}]);

app.controller('ServerTermListCtrl', ['$scope', '$modal', 'config', 'serverService', function ($scope, $modal, config, serverService) {
    //$scope.web_terminal_uri = 'ws://' + config.hostname + ':' + config.port + '/terminal?uuid=' + server.uuid;

    $scope.terms = [];
    $scope.servers = [];
    $scope.select = {};

    serverService.all().then(function (servers) {
        $scope.servers = servers;
    });

    $scope.add = function () {
        $scope.terms.push({
            title: $scope.terms.length + 1 + '. ' + $scope.select.server.title,
            uri: 'ws://' + config.hostname + ':' + config.port + '/terminal?uuid=' + $scope.select.server.uuid
        })
    };

    $scope.close = function (index, title) {
        $scope.showConfirm('<p>请确认是否是要断开服务器连接:' + title + '?</p>').result.then(function (data) {
            if (data) {
                $scope.terms.splice(index, 1);
            }
        });

    };
}]);
