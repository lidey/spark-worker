app.controller('DatabaseCtrl', ['$scope', 'databaseService', '$timeout', '$modal', function ($scope, databaseService, $timeout, $modal) {
    var tree;
    $scope.database_data = [];
    $scope.database_tree = tree = {};
    $scope.reload = function () {
        $scope.database_data = [];
        var data_root = {
            uid: 'root-node',
            type: 'root',
            label: '数据库链接',
            icon: 'fa fa-folder-o'
        };
        databaseService.tree().then(function (data) {
            data_root.children = data;
            $scope.database_data = [data_root];
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
    $scope.database_tree_handler = function (branch) {
        if (branch.type != null) {
            $scope.branch = branch;
            $scope.$broadcast('branch', branch);
        }
    };

    $scope.add_database = function () {
        $scope.edit_database({'data': {}});
    };

    $scope.edit_database = function (branch) {
        $modal.open({
            templateUrl: 'static/tpl/database/database.info.html',
            controller: 'DatabaseEditCtrl',
            size: 'lg',
            resolve: {
                branch: function () {
                    return branch;
                }
            }
        }).result.then(function (message) {
            if (message.success) {
                $scope.showMessage(message);
                $scope.reload();
            }
        });
    };

    $scope.delete_database = function (branch) {
        $scope.showConfirm('<p>请确认是否是要删除数据库链接:' + branch.label + '?</p>').result.then(function (data) {
            if (data) {
                databaseService.delete_database(branch.uid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.reload();
                });
            }
        });
    };


    $scope.add_folder = function (db_uuid) {
        $scope.edit_folder({'type': 'folder', 'data': {db_uuid: db_uuid}});
    };

    $scope.edit_folder = function (branch) {
        $modal.open({
            templateUrl: 'static/tpl/database/folder.info.html',
            controller: 'DatabaseEditCtrl',
            size: 'lg',
            resolve: {
                branch: function () {
                    return branch;
                }
            }
        }).result.then(function (message) {
            if (message.success) {
                $scope.showMessage(message);
                $scope.reload();
            }
        });
    };

    $scope.delete_folder = function (branch) {
        $scope.showConfirm('<p>请确认是否是要删除目录:' + branch.label + '?</p>').result.then(function (data) {
            if (data) {
                databaseService.delete_folder(branch.uid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.reload();
                });
            }
        });
    };

    $scope.import_table = function (branch) {
        $modal.open({
            templateUrl: 'static/tpl/database/table.import.html',
            controller: 'DatabaseTableCtrl',
            size: 'lg',
            resolve: {
                branch: function () {
                    return branch;
                }
            }
        }).result.then(function (message) {
            if (message.success) {
                $scope.showMessage(message);
                $scope.reload();
            }
        });
    };

}]);


app.controller('DatabaseEditCtrl', ['$scope', 'databaseService', '$modalInstance', 'branch', function ($scope, databaseService, $modalInstance, branch) {

    $scope.alerts = [];

    if (branch.type == 'database')
        $scope.database = branch.data;
    if (branch.type == 'folder')
        $scope.folder = branch.data;

    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.save_database = function () {
        databaseService.save_database($scope.database).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

    $scope.save_folder = function () {
        databaseService.save_folder($scope.folder).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };
}]);


app.controller('DatabaseIndexCtrl', ['$scope', 'databaseService', '$compile', '$modal', function ($scope, databaseService, $compile, $modal) {

    $scope.database_detail = false;
    $scope.database_table = false;
    $scope.tableGrid = {};

    $scope.testDatabase = function () {
        databaseService.test($scope.database.uuid).then(function (data) {
            $scope.showMessage(data);
        });
    };


    $scope.$on('branch', function (event, branch) {
        if (branch == null || branch.type == 'root') {
            $scope.database_detail = false;
            $scope.database_table = false;
            return;
        }
        if (branch.type == 'database') {
            $scope.database = branch.data;
            $scope.database_detail = true;
            $scope.database_table = false;
            return;
        }
        if (branch.type.indexOf('folder') == 0) {
            $scope.database_detail = false;
            $scope.database_table = true;

            var folder_uuid = '';
            if (branch.type == 'folder')
                folder_uuid = branch.data.uuid;
            var url = 'database/' + branch.data.db_uuid + '/table_list?folder_uuid=' + folder_uuid;

            if ($scope.tableGrid.tables == undefined) {
                $scope.dt_option = {
                    'language': {
                        'url': 'static/vendor/jquery/datatables/i18n/zh_CN.json'

                    },
                    ajax: {
                        url: url,
                        dataSrc: 'tables'
                    },
                    columns: [
                        {title: '主键', data: 'uuid', visible: false},
                        {title: '名称', data: 'name', width: '40%'},
                        {title: '类型', data: 'type', width: '20%'},
                        {title: '创建时间', data: 'created_time', width: '20%'}
                    ],
                    columnDefs: [
                        {
                            targets: [1],
                            render: function (data, type, row) {
                                return '<a ng-click="edit_table(\'' + row.uuid + '\')" class="text-info"><i class="fa fa-table m-r-xs"></i>' + data + '</a>';
                            }
                        },
                        {
                            targets: [2],
                            render: function (data, type, row) {
                                if (data == 'TABLE')
                                    return '数据表';
                            }
                        },
                        {
                            targets: [3],
                            render: function (data, type, row) {
                                return new Date(parseInt(data)).toLocaleString().replace(/:\d{1,2}$/, ' ');
                            }
                        },
                        {
                            title: '操作', width: '20%', targets: [4], data: 'uuid', orderable: false,
                            render: function (data, type, row) {
                                return '<a ng-click="delete_table(\'' + data + '\',\'' + row.name + '\')" class="text-warning"><i class="fa fa-times m-r-xs"></i>删除</a>';
                            }
                        }
                    ],
                    "fnCreatedRow": function (nRow, aData, iDataIndex) {
                        $compile(nRow)($scope);
                    }
                };
            } else {
                $scope.tableGrid.tables.api().ajax.url(url).load();
            }
            return;
        }
    });

    $scope.edit_table = function (uuid) {
        $modal.open({
            templateUrl: 'static/tpl/database/table.columns.html',
            controller: 'DatabaseTableCtrl',
            size: 'lg',
            resolve: {
                branch: function () {
                    return {uid: uuid, type: 'table', data: {uuid: uuid}};
                }
            }
        })
    };

    $scope.delete_table = function (uuid, name) {
        $scope.showConfirm('<p>请确认是否是要删除数据表:' + name + '?</p>').result.then(function (data) {
            if (data) {
                databaseService.delete_table(uuid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.tableGrid.tables.api().ajax.reload();
                });
            }
        });
    };

}]);

app.controller('DatabaseTableCtrl', ['$scope', 'databaseService', '$modalInstance', '$compile', 'branch', function ($scope, databaseService, $modalInstance, $compile, branch) {

    $scope.alerts = [];
    $scope.table_names = [];
    $scope.grid = {};

    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    if (branch.type.indexOf('folder') == 0) {
        $scope.table = {};
        $scope.table.db_uuid = branch.data.db_uuid;
        if (branch.type == 'folder')
            $scope.table.folder_uuid = branch.uid;

        databaseService.table_name_list($scope.table.db_uuid).then(function (data) {
            $scope.table_names = data;
        });
    }

    $scope.import = function () {
        databaseService.import_tables($scope.table).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };


    if (branch.type == 'table') {
        $scope.table = branch.data;
        $scope.dt_option = {
            'language': {
                'url': 'static/vendor/jquery/datatables/i18n/zh_CN.json'
            },
            ajax: {
                url: 'database/' + branch.uid + '/column_list',
                dataSrc: 'columns'
            },
            columns: [
                {title: '主键', data: 'uuid', visible: false},
                {title: '字段名', data: 'field', width: '40%'},
                {title: '类型', data: 'key', width: '20%'},
                {title: '字段类型', data: 'type', width: '20%'}
            ],
            columnDefs: [
                {
                    title: '操作', width: '20%', targets: [4], data: 'uuid', orderable: false,
                    render: function (data, type, row) {
                        return '<a ng-click="delete_column(\'' + data + '\',\'' + row.name + '\')" class="text-warning"><i class="fa fa-times m-r-xs"></i>删除</a>';
                    }
                }
            ],
            dom: "t<'row'<'col-xs-6'i><'col-xs-6'p>>",
            "fnCreatedRow": function (nRow, aData, iDataIndex) {
                $compile(nRow)($scope);
            }
        };
    }

    $scope.delete_column = function (uuid) {
        databaseService.delete_column(uuid).then(function (message) {
            $scope.alerts.push({type: 'success', msg: message.content});
            $scope.grid.columns.api().ajax.reload();
        });
    };

    $scope.reload_column = function (uuid) {
        databaseService.column_reload(uuid).then(function (message) {
            $scope.alerts.push({type: 'success', msg: message.content});
            $scope.grid.columns.api().ajax.reload();
        });
    };
}]);