app.controller('ModelCtrl', ['$scope', 'modelService', '$timeout', '$modal', function ($scope, modelService, $timeout, $modal) {
    var tree;
    $scope.model_data = [];
    $scope.model_tree = tree = {};
    $scope.reload = function () {
        $scope.model_data = [];
        var data_root = {
            uid: 'root-node',
            type: 'root',
            label: '数据模型目录',
            icon: 'fa fa-folder-o'
        };
        modelService.tree().then(function (data) {
            data_root.children = data;
            $scope.model_data = [data_root];
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

    $scope.model_tree_handler = function (branch) {
        if (branch.type != null) {
            $scope.branch = branch;
            $scope.$broadcast('branch', branch);
        }
    };


    $scope.add_category = function (branch) {
        $scope.edit_category({type: 'category_add', uid: branch.uid,label:branch.label});
    };

    $scope.edit_category = function (branch) {
        $modal.open({
            templateUrl: 'static/tpl/database/category.info.html',
            controller: 'ModelEditCtrl',
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

    $scope.delete_category = function (branch) {
        $scope.showConfirm('<p>请确认是否是要删除模型目录:' + branch.label + '?</p>').result.then(function (data) {
            if (data) {
                modelService.delete_category(branch.uid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.reload();
                });
            }
        });
    };

    $scope.add_model = function () {
        $scope.edit_model({'data': {}});
    };

    $scope.edit_model = function (branch) {
        $modal.open({
            templateUrl: 'static/tpl/database/model.info.html',
            controller: 'ModelEditCtrl',
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

    $scope.delete_model = function (branch) {
        $scope.showConfirm('<p>请确认是否是要删除模型:' + branch.label + '?</p>').result.then(function (data) {
            if (data) {
                modelService.delete_model(branch.uid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.reload();
                });
            }
        });
    };

}]);


app.controller('ModelEditCtrl', ['$scope', 'modelService', '$modalInstance', 'branch', function ($scope, modelService, $modalInstance, branch) {

    $scope.alerts = [];
    console.log(branch)
    if (branch.type == 'category_add' && branch.uid != 'root-node')
        $scope.category = {p_uuid: branch.uid, p_title: branch.label};
    if (branch.type == 'category')
        $scope.category = branch.data;
    if (branch.type == 'model')
        $scope.model = branch.data;

    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.save_category = function () {
        modelService.save_category($scope.category).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

    $scope.save_model = function () {
        modelService.save_model($scope.model).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

}]);


app.controller('ModelIndexCtrl', ['$scope', 'modelService', '$compile', '$modal', function ($scope, modelService, $compile, $modal) {

    $scope.category_table = false;
    $scope.modelGrid = {};

    $scope.$on('branch', function (event, branch) {
        if (branch == null || branch.type == 'root') {
            $scope.category_table = false;
            return;
        }

        if (branch.type == 'category') {
            $scope.category_table = true;

            var folder_uuid = '';
            if (branch.type == 'folder')
                folder_uuid = branch.data.uuid;
            var url = 'database/' + branch.data.db_uuid + '/table_list?folder_uuid=' + folder_uuid;

            if ($scope.modelGrid.models == undefined) {
                $scope.dt_option = {
                    'language': {
                        'url': 'static/vendor/jquery/datatables/i18n/zh_CN.json'

                    },
                    ajax: {
                        url: url,
                        dataSrc: 'models'
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
                $scope.modelGrid.models.api().ajax.url(url).load();
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
                modelService.delete_table(uuid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.modelGrid.models.api().ajax.reload();
                });
            }
        });
    };

}]);