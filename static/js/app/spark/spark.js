app.controller('SparkCtrl', ['$scope', 'sparkService', '$stateParams', function ($scope, sparkService, $stateParams) {

    $scope.refresh = function () {
        sparkService.all().then(function (sparks) {
            $scope.sparks = sparks;
        });
    };

    $scope.selectSpark = function (spark) {
        angular.forEach($scope.sparks, function (tmp) {
            if (tmp.uuid == spark.uuid) {
                tmp.selected = true;
                tmp.color = 'success';
                $scope.spark = tmp;
                $scope.$broadcast('spark', tmp);
            } else {
                tmp.selected = false;
                tmp.color = 'info';
            }

        });
    };
}]);

app.controller('SparkJobListCtrl', ['$scope', 'sparkService', '$compile', '$modal', function ($scope, sparkService, $compile, $modal) {
    $scope.spark = undefined;
    $scope.jobGrid = {};
    $scope.$on('spark', function (event, data) {

        sparkService.get(data.uuid).then(function (spark) {
            $scope.spark = data;
            var url = 'spark/job/list?s_uuid=' + spark.uuid;
            if ($scope.jobGrid.jobs == undefined) {
                $scope.dt_option = {
                    'language': {
                        'url': 'static/vendor/jquery/datatables/i18n/zh_CN.json'

                    },
                    ajax: {
                        url: url,
                        dataSrc: 'jobs'
                    },
                    columns: [
                        {title: '主键', data: 'uuid', visible: false},
                        {title: '名称', data: 'title', width: '35%'},
                        {title: '节点', data: 'master', width: '20%'},
                        {title: '创建时间', data: 'created_time', width: '15%'}
                    ],
                    columnDefs: [
                        {
                            targets: [1],
                            render: function (data, type, row) {
                                return '<a ng-click="edit_job(\'' + row.uuid + '\')" class="text-info"><i class="fa icon-ghost m-r-xs"></i>' + data + '</a>';
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
                                return '<a ng-click="run_spark(\'' + data + '\')" class="text-info m-r-md"><i class="fa  fa-play m-r-xs"></i>执行</a>' +
                                    '<a ng-click="designer_job(\'' + data + '\')" class="text-info m-r-md"><i class="fa  fa-calendar m-r-xs"></i>调度</a>' +
                                    '<a ng-click="designer_job(\'' + data + '\')" class="text-info m-r-md"><i class="fa fa-sliders m-r-xs"></i>设计</a>' +
                                    '<a ng-click="delete_job(\'' + data + '\',\'' + row.title + '\')" class="text-warning"><i class="fa fa-times m-r-xs"></i>删除</a>';
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
        });
    });

    $scope.$on('message', function (event, data) {
        $scope.message = data;
    });

    $scope.add_job = function () {
        $scope.edit_job(null);
    };
    $scope.edit_job = function (uuid) {
        $modal.open({
            templateUrl: 'static/tpl/spark/job.info.html',
            controller: 'SparkJobCtrl',
            size: 'lg',
            resolve: {
                spark: function () {
                    return $scope.spark;
                },
                uuid: function () {
                    return uuid;
                },
                deps: ['$ocLazyLoad',
                    function ($ocLazyLoad) {
                        return $ocLazyLoad.load('angularFileUpload');
                    }]
            }
        }).result.then(function (message) {
            $scope.showMessage(message);
            if (message.success) {
                $scope.jobGrid.jobs.api().ajax.reload();
            }
        });
    };
    $scope.designer_job = function (uuid) {
        $modal.open({
            templateUrl: 'static/tpl/spark/job.designer.html',
            controller: 'SparkJobCtrl',
            size: 'lg',
            resolve: {
                spark: function () {
                    return $scope.spark;
                },
                uuid: function () {
                    return uuid;
                },
                deps: ['$ocLazyLoad',
                    function ($ocLazyLoad) {
                        return $ocLazyLoad.load(['angularFileUpload', 'ui.select']);
                    }]
            }
        }).result.then(function (message) {
            $scope.showMessage(message);
            if (message.success) {
                $scope.jobGrid.jobs.api().ajax.reload();
            }
        });
    };

    $scope.delete_job = function (uuid, title) {
        $scope.showConfirm('请确认是否删除服务器:' + title).result.then(function (data) {
            if (data) {
                sparkService.delete_job(uuid).then(function (message) {
                    $scope.showMessage(message);
                    $scope.jobGrid.jobs.api().ajax.reload();
                });
            }

        }, function () {
        });
    };

    $scope.run_spark = function (uuid) {
        sparkService.run_spark(uuid).then(function (message) {
            $scope.showMessage(message);
        })
    };
}]);

app.controller('SparkJobCtrl', ['$scope', 'sparkService', '$modalInstance', '$modal', 'FileUploader', 'spark', 'uuid', function ($scope, sparkService, $modalInstance, $modal, FileUploader, spark, uuid) {
    $scope.alerts = [];
    $scope.spark = spark;

    var uploader = $scope.uploader = new FileUploader({
        url: 'spark/job/upload_jar',
        autoUpload: true
    });

    if (uuid == null) {
        $scope.job = {s_uuid: spark.uuid, memory: 512, processor: 1, master: spark.rest_url};
    } else {
        sparkService.get_job(uuid).then(function (data) {
            $scope.job = data;
            $scope.job.s_uuid = spark.uuid;
            $scope.uploader.headers = {'uuid': $scope.job.uuid};
            if ($scope.job.jars.length > 0)
                $scope.load_classes();
        });
    }
    $scope.closeAlert = function (index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss();
    };

    $scope.init_slider = function () {
        angular.element("#memory-slider").on('slideStop', function (data) {
            $scope.$apply(function () {
                $scope.job.memory = data.value;
            });
        });

        angular.element("#processor-slider").on('slideStop', function (data) {
            $scope.$apply(function () {
                $scope.job.processor = data.value;
            });
        });
    };

    $scope.remove_jar = function (jar) {
    };

    // FILTERS

    uploader.filters.push({
        name: 'jarFilter',
        fn: function (item /*{File|FileLikeObject}*/, options) {
            var uploadFileExtend = ".jar,";

            //判断后缀
            var fileExtend = item.name.substring(item.name.lastIndexOf('.')).toLowerCase();
            //可以对fileExtend（文件后缀<.xxx>） 进行判断 处理
            return uploadFileExtend.indexOf(fileExtend) > -1
        }
    });

    uploader.onSuccessItem = function (fileItem, response, status, headers) {
        if (response.success) {
            fileItem.remove();
            for (var i = 0; i < $scope.job.jars.length; i++)
                if ($scope.job.jars[i] == response.file_name)
                    $scope.job.jars.splice(i, 1);
            $scope.job.jars.push(response.file_name);
            $scope.load_classes();
        }
    };

    $scope.load_classes = function () {
        sparkService.open_jars($scope.job.uuid).then(function (classes) {
            console.log(classes);
            $scope.classes = classes;
            for (var i = 0; i < classes.length; i++) {
                if (classes[i].name == $scope.job.main_class)
                    $scope.job.class = classes[i];
            }
        });
    };

    $scope.remove_jar = function (index, filename) {
        sparkService.remove_jar($scope.job.uuid, filename).then(function (message) {
            if (message.success) {
                $scope.job.jars.splice(index, 1);
                $scope.load_classes();
            } else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

    $scope.save_job = function () {
        sparkService.save_job($scope.job).then(function (message) {
            if (message.success)
                $modalInstance.close(message);
            else
                $scope.alerts.push({type: 'danger', msg: message.content})
        });
    };

}]);

app.controller('SparkJobLogsCtrl', ['$scope', 'sparkService', '$modalInstance', 'config', 'content', function ($scope, sparkService, $modalInstance, config, content) {

    $scope.cancel = function () {
        $modalInstance.dismiss();
    };

    $scope.logs = content.replace(new RegExp(/(\tat)/g), '&nbsp;&nbsp;&nbsp;&nbsp;').split('\n');

}]);


app.controller('SparkLogListCtrl', ['$scope', 'sparkService', '$compile', '$modal', function ($scope, sparkService, $compile, $modal) {

    $scope.jobGrid = {};
    $scope.dt_option = {
        'language': {
            'url': 'static/vendor/jquery/datatables/i18n/zh_CN.json'

        },
        ajax: {
            url: 'spark/job/log_list',
            dataSrc: 'logs'
        },
        columns: [
            {title: '主键', data: 'uuid', visible: false},
            {title: '名称', data: 'title', width: '40%'},
            {title: '作业ID', data: 'app_id', width: '20%'},
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
                targets: [4],
                render: function (data, type, row) {
                    return new Date(parseInt(data)).toLocaleString().replace(/:\d{1,2}$/, ' ');
                }
            },
            {
                title: '操作', width: '15%', targets: [5], data: 'uuid', orderable: false,
                render: function (data, type, row) {
                    return '<a ng-click="show_out(\'' + data + '\')" class="text-info m-r-md"><i class="fa  fa-eye m-r-xs"></i>输出</a>' +
                        '<a ng-click="show_log(\'' + data + '\',\'' + row.title + '\')" class="text-info"><i class="fa fa-eye m-r-xs"></i>日志</a>';
                }
            }
        ],
        order: [[4, "desc"]],
        "fnCreatedRow": function (nRow, aData, iDataIndex) {
            $compile(nRow)($scope);
        }
    };

    $scope.show_out = function (uuid) {
        sparkService.get_log(uuid).then(function (log) {
            openLog(log.std_out);
        })
    };


    $scope.show_log = function (uuid) {
        sparkService.get_log(uuid).then(function (log) {
            openLog(log.std_err);
        })
    };

    function openLog(content) {
        $modal.open({
            templateUrl: 'static/tpl/spark/job.log.html',
            controller: 'SparkJobLogsCtrl',
            size: 'lg',
            resolve: {
                content: function () {
                    return content;
                }
            }
        })
    };

}]);
