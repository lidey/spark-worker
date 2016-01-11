app.controller('ModelCtrl', ['$scope', 'modelService', '$timeout', '$modal', function ($scope, modelService, $timeout, $modal) {
    var tree;
    $scope.model_data = [];
    $scope.model_tree = tree = {};
    $scope.reload = function () {
        $scope.model_data = [];
        var data_root = {
            uid: 'root-node',
            type: 'root',
            label: '数据模型分类目录',
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
        $scope.edit_category({type: 'category_add', uid: branch.uid, label: branch.label});
    };

    $scope.edit_category = function (branch) {
        $modal.open({
            templateUrl: 'static/tpl/database/category.info.html',
            controller: 'ModelEditCtrl',
            size: '',
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

    $scope.add_model = function (c_uuid) {
        open_model({type: 'model', 'data': {c_uuid: c_uuid, type: 'TABLE'}});
    };


    $scope.edit_model = function (uuid) {
        modelService.get_model(uuid).then(function (model) {
            open_model({type: 'model', 'data': model});
        });
    };

    function open_model(branch) {
        $modal.open({
            templateUrl: 'static/tpl/database/model.info.html',
            controller: 'ModelEditCtrl',
            size: '',
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
    }

    $scope.delete_model = function (uuid, title) {
        $scope.showConfirm('<p>请确认是否是要删除数据模型:' + title + '?</p>').result.then(function (data) {
            if (data) {
                modelService.delete_model(uuid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.reload();
                });
            }
        });
    };

}]);


app.controller('ModelEditCtrl', ['$scope', 'modelService', 'databaseService', '$modalInstance', 'branch', function ($scope, modelService, databaseService, $modalInstance, branch) {

    $scope.alerts = [];

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

    if (branch.type == 'category_add' && branch.uid != 'root-node')
        $scope.category = {p_uuid: branch.uid, p_title: branch.label};
    if (branch.type == 'category')
        $scope.category = branch.data;

    $scope.save_model = function () {
        modelService.save_model($scope.model).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

    if (branch.type == 'model') {
        $scope.model = branch.data;
        databaseService.database_list().then(function (databases) {
            $scope.databases = databases;
        })
    }

    $scope.change_folder = function (f_uuid, d_uuid) {
        databaseService.table_list({type: 'folder', data: {uuid: f_uuid, db_uuid: d_uuid}}).then(function (tables) {
            $scope.tables = tables;
        });
    };
    $scope.import_tables = function (modelTable) {
        modelService.save_modelTable(modelTable).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

    if (branch.type == 'import') {
        $scope.modelTable = {d_uuid: branch.data.d_uuid, m_uuid: branch.data.uuid};
        databaseService.folder_list(branch.data.d_uuid).then(function (folders) {
            $scope.folders = folders;
        });
        $scope.change_folder('', branch.data.d_uuid);
    }

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

            var url = 'database/' + branch.data.uuid + '/model_list';

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
                        {title: '名称', data: 'title', width: '40%'},
                        {title: '类型', data: 'type', width: '10%'},
                        {title: '创建时间', data: 'created_time', width: '20%'}
                    ],
                    columnDefs: [
                        {
                            targets: [1],
                            render: function (data, type, row) {
                                return '<a ng-click="option_model(\'' + row.uuid + '\')" class="text-info"><i class="fa fa-cube m-r-xs"></i>' + data + '</a>';
                            }
                        },
                        {
                            targets: [2],
                            render: function (data, type, row) {
                                switch (data) {
                                    case 'TABLE':
                                        return '数据表';
                                        break;
                                    default:
                                        return '';
                                }
                            }
                        },
                        {
                            targets: [3],
                            render: function (data, type, row) {
                                return new Date(parseInt(data)).toLocaleString().replace(/:\d{1,2}$/, ' ');
                            }
                        },
                        {
                            title: '操作', width: '30%', targets: [4], data: 'uuid', orderable: false,
                            render: function (data, type, row) {
                                return '<a ng-click="edit_model(\'' + data + '\')" class="text-info m-r-md"><i class="fa fa-pencil m-r-xs"></i>编辑</a>'
                                    + '<a ng-click="delete_model(\'' + data + '\',\'' + row.title + '\')" class="text-warning"><i class="fa fa-times m-r-xs"></i>删除</a>';
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

    $scope.option_model = function (uuid) {
        modelService.get_model(uuid).then(function (model) {
            $modal.open({
                templateUrl: 'static/tpl/database/model.option.html',
                controller: 'ModelOptionCtrl',
                size: 'lg',
                resolve: {
                    model: function () {
                        return model;
                    }
                }
            });
        });
    }

}]);


app.controller('ModelOptionCtrl', ['$scope', 'modelService', 'databaseService', '$modalInstance', '$modal', '$timeout', 'model', function ($scope, modelService, databaseService, $modalInstance, $modal, $timeout, model) {

    $scope.alerts = [];
    $scope.model = model;

    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.showMessage = function (message) {
        return $modal.open({
            templateUrl: 'messageModalContent.html',
            controller: 'ModalCtrl',
            size: '',
            resolve: {
                message: function () {
                    return message;
                }
            }
        });
    };

    $scope.showConfirm = function (content) {
        return $modal.open({
            templateUrl: 'confirmModalContent.html',
            controller: 'ModalCtrl',
            size: '',
            resolve: {
                message: function () {
                    return {success: false, content: content};
                }
            }
        });
    };

    var tree;
    $scope.table_data = [];
    $scope.table_tree = tree = {};
    $scope.reload = function () {
        modelService.table_tree(model.uuid).then(function (data) {
            $scope.table_data = data;
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

    $scope.table_tree_handler = function (branch) {
        if (branch.type != null) {
            $scope.branch = branch;
            $scope.$broadcast('branch', branch);
        }
    };

    $scope.import_table = function (model) {
        $modal.open({
            templateUrl: 'static/tpl/database/model.table.import.html',
            controller: 'ModelEditCtrl',
            size: '',
            resolve: {
                branch: function () {
                    return {type: 'import', 'data': model};
                }
            }
        }).result.then(function (message) {
            if (message.success)
                $scope.reload();
        });
    };

    $scope.indexes = [];
    modelService.modelIndex_list($scope.model.uuid).then(function (indexes) {
        $scope.indexes = indexes;
    });

    $scope.onIndexDrop = function (event, data, indexes) {
        modelService.save_modelIndex({m_uuid: $scope.model.uuid, c_uuid: data.data.uuid}).then(function (message) {
            if (message.success) {
                indexes.push(message.index);
            }
            $scope.showMessage(message);
        })
    };
    $scope.removeIndex = function (index, $index) {
        $scope.showConfirm('请确认是否要删除指标:' + index.c_field + '?').result.then(function (data) {
            if (data) {
                modelService.delete_index(index.uuid).then(function (message) {
                    if (message.success) {
                        $scope.showMessage(message);
                        $scope.indexes.splice($index, 1);
                    }
                })
            }
        });
    };

}]);