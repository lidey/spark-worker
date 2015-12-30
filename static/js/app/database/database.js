app.controller('DatabaseCtrl', ['$scope', 'databaseService', '$timeout', '$modal', function ($scope, databaseService, $timeout, $modal) {
    var tree;
    $scope.my_data = [];
    $scope.my_tree = tree = {};
    $scope.reload = function () {
        $scope.my_data = [];
        var data_root = {
            uid: 'root-node',
            type: 'root',
            label: '数据库链接',
            icon: 'fa fa-folder-o'
        };
        databaseService.tree().then(function (data) {
            data_root.children = data;
            $scope.my_data = [data_root];
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
    $scope.my_tree_handler = function (branch) {
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
            templateUrl: 'static/tpl/database/Folder.info.html',
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
        $scope.showConfirm('<p>请确认是否是要目录:' + branch.label + '?</p>').result.then(function (data) {
            if (data) {
                databaseService.delete_folder(branch.uid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.reload();
                });
            }
        });
    };

    $scope.import_table = function (branch) {
    };

}]);

app.controller('DatabaseIndexCtrl', ['$scope', 'databaseService', function ($scope, databaseService) {
    $scope.database_detail = false;
    $scope.database_table = false;
    $scope.tableGrid = {};
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
            $scope.ook = function(){
                console.log($scope.tableGrid)
                console.log($scope.tableGrid.Td123.api())
                console.log($scope.tableGrid.Td123.api().ajax.url())
            };
            $scope.dt_option = {
                sAjaxSource: 'static/vendor/jquery/datatables/datatable.json',
                aoColumns: [
                    {mData: 'engine'},
                    {mData: 'browser'},
                    {mData: 'platform'},
                    {mData: 'version'},
                    {mData: 'grade'}
                ]
            };

            return;
        }
    });

    $scope.testDatabase = function () {
        databaseService.test($scope.database.uuid).then(function (data) {
            $scope.showMessage(data);
        });
    };
}]);

app.controller('DatabaseEditCtrl', ['$scope', 'databaseService', '$modalInstance', 'branch', function ($scope, databaseService, $modalInstance, branch) {

    if (branch.type == 'database')
        $scope.database = branch.data;
    if (branch.type == 'folder')
        $scope.folder = branch.data;
    $scope.alerts = [];

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
