app.controller('SchedulerCtrl', ['$scope', 'schedulerService', function ($scope, schedulerService) {

}]);


app.controller('SchedulerListCtrl', ['$scope', 'schedulerService', '$compile', '$modal', function ($scope, schedulerService, $compile, $modal) {

    $scope.grid = {};
    $scope.dt_option = {
        'language': {
            'url': 'static/vendor/jquery/datatables/i18n/zh_CN.json'
        },
        ajax: {
            url: 'scheduler/list',
            dataSrc: 'schedulers'
        },
        columns: [
            {title: '主键', data: 'uuid', visible: false},
            {title: '名称', data: 'title', width: '25%'},
            {title: 'cron', data: 'cron', width: '20%'},
            {title: '类型', data: 'type', width: '10%'},
            {title: '状态', data: 'status', width: '10%'},
            {title: '创建时间', data: 'created_time', width: '15%'}
        ],
        columnDefs: [
            {
                targets: [1],
                render: function (data, type, row) {
                    return '<i class="fa fa-bug m-r-xs"></i>' + data;
                }
            },
            {
                targets: [2],
                render: function (data, type, row) {
                    if (data != undefined)
                        return data.second + ' ' + data.minute + ' ' + data.hour + ' ' + data.day + ' ' + data.month + ' ' + data.week + ' ' + data.year;
                    else
                        return '为定义';
                }
            },
            {
                targets: [4],
                render: function (data, type, row) {
                    if (data == 'DISABLE')
                        return '停用';
                    if (data == 'ENABLE')
                        return '启用';
                }
            },
            {
                targets: [5],
                render: function (data, type, row) {
                    return new Date(parseInt(data)).toLocaleString().replace(/:\d{1,2}$/, ' ');
                }
            },
            {
                title: '操作', width: '20%', targets: [6], data: 'uuid', orderable: false,
                render: function (data, type, row) {
                    var option = '';
                    if (row.status == 'DISABLE')
                        option += '<a ng-click="startup(\'' + data + '\',\'' + row.title + '\')" class="text-info m-r-md"><i class="glyphicon glyphicon-play m-r-xs"></i>启动</a>';
                    if (row.status == 'ENABLE')
                        option += '<a ng-click="shutdown(\'' + data + '\',\'' + row.title + '\')" class="text-info m-r-md"><i class="glyphicon glyphicon-stop m-r-xs"></i>停止</a>';
                    option += '<a ng-click="cron_scheduler(\'' + data + '\')" class="text-info m-r-md"><i class="fa  fa-calendar m-r-xs"></i>调度</a>';
                    option += '<a ng-click="delete_scheduler(\'' + data + '\',\'' + row.title + '\')" class="text-warning"><i class="fa fa-times m-r-xs"></i>删除</a>';
                    return option;
                }
            }
        ],
        order: [[5, "desc"]],
        "fnCreatedRow": function (nRow, aData, iDataIndex) {
            $compile(nRow)($scope);
        }
    };

    $scope.startup = function (uuid, title) {
        schedulerService.startup(uuid).then(function (message) {
            $scope.showMessage(message);
            if (message.success)
                $scope.grid.achedulers.api().ajax.reload();
        })
    };


    $scope.shutdown = function (uuid, title) {
        schedulerService.shutdown(uuid).then(function (message) {
            $scope.showMessage(message);
            if (message.success)
                $scope.grid.achedulers.api().ajax.reload();
        })
    };

    $scope.add_scheduler = function (type) {
        $scope.edit_scheduler(null, type);
    };

    $scope.edit_scheduler = function (uuid, type) {
        $modal.open({
            templateUrl: 'static/tpl/scheduler/scheduler.info.html',
            controller: 'SchedulerEditCtrl',
            size: 'lg',
            resolve: {
                type: function () {
                    return type;
                },
                uuid: function () {
                    return uuid;
                },
                deps: ['$ocLazyLoad',
                    function ($ocLazyLoad) {
                        return $ocLazyLoad.load(['ui.select']);
                    }]
            }
        }).result.then(function (message) {
            $scope.showMessage(message);
            if (message.success) {
                $scope.grid.achedulers.api().ajax.reload();
            }
        });
    };

    $scope.cron_scheduler = function (uuid) {
        schedulerService.get(uuid).then(function (scheduler) {
            $modal.open({
                templateUrl: 'static/tpl/app.cron.html',
                controller: 'AppCronCtrl',
                size: '',
                resolve: {
                    cron: function () {
                        return scheduler.cron;
                    },
                    deps: ['uiLoad',
                        function (uiLoad) {
                            return uiLoad.load('static/js/controllers/app-cron.js');
                        }]
                }
            }).result.then(function (cron) {
                cron.s_uuid = uuid;
                schedulerService.set_cron(cron).then(function (message) {
                    $scope.showMessage(message);
                    if (message.success)
                        $scope.grid.achedulers.api().ajax.reload();
                })
            });
        })

    };

    $scope.delete_scheduler = function (uuid, name) {
        $scope.showConfirm('请确认是否删除任务:' + name).result.then(function (data) {
            if (data) {
                schedulerService.delete(uuid).then(function (message) {
                    $scope.showMessage(message);
                    if (message.success)
                        $scope.grid.achedulers.api().ajax.reload();
                });
            }

        }, function () {
        });
    };
}]);

app.controller('SchedulerEditCtrl', ['$scope', 'schedulerService', '$modalInstance', 'uuid', 'type', 'sparkService', function ($scope, schedulerService, $modalInstance, uuid, type, sparkService) {
    $scope.alerts = [];

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    if (uuid != null) {
        schedulerService.get(uuid).then(function (data) {
            $scope.scheduler = data;
        });
    } else {
        $scope.scheduler = {};
        $scope.scheduler.type = type;
        if (type == 'SPARK') {
            sparkService.job_all().then(function (jobs) {
                $scope.spark_jobs = jobs
            })
        }
    }

    $scope.save_scheduler = function () {
        schedulerService.save($scope.scheduler).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

}]);


app.controller('SchedulerLogListCtrl', ['$scope', 'schedulerService', '$compile', '$modal', function ($scope, schedulerService, $compile, $modal) {

    $scope.grid = {};
    $scope.dt_option = {
        'language': {
            'url': 'static/vendor/jquery/datatables/i18n/zh_CN.json'
        },
        ajax: {
            url: 'scheduler/log_list',
            dataSrc: 'logs'
        },
        columns: [
            {title: '主键', data: 'uuid', visible: false},
            {title: '名称', data: 'scheduler', width: '25%'},
            {title: '编码', data: 'code', width: '20%'},
            {title: '状态', data: 'status', width: '10%'},
            {title: '创建时间', data: 'created_time', width: '15%'}
        ],
        columnDefs: [
            {
                targets: [1],
                render: function (data, type, row) {
                    return '<i class="fa fa-bug m-r-xs"></i>' + data.title;
                }
            },
            {
                targets: [2],
                render: function (data, type, row) {
                    if (data == 1024)
                        return '正常';
                    if (data == 2048)
                        return '系统异常';
                }
            },
            {
                targets: [3],
                render: function (data, type, row) {
                    if (data == 'SUCCESS')
                        return '成功';
                    if (data == 'ERROR')
                        return '失败';
                }
            },
            {
                targets: [4],
                render: function (data, type, row) {
                    return new Date(parseInt(data)).toLocaleString().replace(/:\d{1,2}$/, ' ');
                }
            },
            {
                title: '操作', width: '20%', targets: [5], data: 'uuid', orderable: false,
                render: function (data, type, row) {
                    var option = '';
                    if (row.status == 'ERROR')
                        option += '<a ng-click="show_err(\'' + data + '\')" class="text-info m-r-md"><i class="fa  fa-eye m-r-xs"></i>日志</a>';
                    return option;
                }
            }
        ],
        order: [[4, "desc"]],
        "fnCreatedRow": function (nRow, aData, iDataIndex) {
            $compile(nRow)($scope);
        }
    };

    $scope.show_err = function (uuid) {
        $modal.open({
            templateUrl: 'static/tpl/scheduler/scheduler.log.html',
            controller: 'SchedulerLogsCtrl',
            size: 'lg',
            resolve: {
                uuid: function () {
                    return uuid;
                }
            }
        })
    };

}]);

app.controller('SchedulerLogsCtrl', ['$scope', 'schedulerService', '$modalInstance', 'uuid', function ($scope, schedulerService, $modalInstance, uuid) {

    $scope.logs = [];
    $scope.cancel = function () {
        $modalInstance.dismiss();
    };
    schedulerService.get_log(uuid).then(function (log) {
        $scope.logs = log.std_err.split('\n');
    })


}]);