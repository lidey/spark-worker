app.controller('SchedulerCtrl', ['$scope', 'schedulerService', '$location', "jobs", '$http', function ($scope, schedulerService, $location, jobs, $http) {
    var jId;
    $scope.refresh = function () {
        schedulerService.all().then(function (req) {
            jobs.all().then(function (reqj) {
                var jobsSC;
                if (reqj.data.success) {
                    jobsSC = reqj.data.list;
                } else {
                    $scope.showMessage({content: reqj.data.message})
                }
                //$scope.jobs = jobsSC;
                $scope.$broadcast('jobitems', /*$scope.*/jobsSC);
            })
            jobs.script_all(jId);
            $scope.schedulers = req;
            /*angular.forEach($scope.schedulers, function (test){
             console.error("req:>>>"+test)
             })*/
            //获取页面默认选中的第一个显示其job列表
            /*var jobsList = [];
             jobs.get().then(function (reqJobs){
             console.info("jId>>>>>>>>>>>>>>>>."+jId)
             console.log("jobInfo>>>"+reqJobs.data)
             jobsList.push(reqJobs.data)
             $scope.$broadcast('firstJob',jobsList)
             console.error("firstJob:"+jobsList[0])
             });*/
            if ($scope.scheduler == undefined)
                $scope.scheduler = $scope.schedulers[0];

            else
                angular.forEach($scope.schedulers, function (reqs) {
                    if (reqs.uuid == $scope.scheduler.uuid)
                        reqs.selected = true;
                });
            //默认显示的scheduler的job列表——————开始
            var jobIdArray = $scope.scheduler.jobId.split(',')
            var jobsList = new Array();
            if (jobIdArray.length >= 1) {
                for (var i = 0; i < jobIdArray.length; i++) {
                    jobs.get(jobIdArray[i]).then(function (reqJobs) {
                        jobsList.push(reqJobs.data)
                    })
                }
                $scope.$broadcast('firstJob', jobsList)
            } else {
                jobs.get(jobIdArray).then(function (reqJobs) {
                    jobsList.push(reqJobs.data)
                    $scope.$broadcast('firstJob', jobsList)
                })
            }
            //默认显示的scheduler的job列表——————结束
            $scope.scheduler.selected = true;
            $scope.$broadcast('scheduler', $scope.scheduler);
            //$scope.job.selected = true;
            $scope.$broadcast('job', $scope.job);
        });

    };


    $scope.selectScheduler = function (scheduler) {
        angular.forEach($scope.schedulers, function (scheduler) {
            scheduler.selected = false;
        });
        $scope.scheduler = scheduler;
        var jobIdArray = $scope.scheduler.jobId.split(',')
        var jobsList = new Array();
        if (jobIdArray.length >= 1) {
            for (var i = 0; i < jobIdArray.length; i++) {
                jobs.get(jobIdArray[i]).then(function (reqJobs) {
                    jobsList.push(reqJobs.data)
                })
            }
            $scope.$broadcast('firstJob', jobsList)
        } else {
            jobs.get(jobIdArray).then(function (reqJobs) {
                jobsList.push(reqJobs.data)
                $scope.$broadcast('firstJob', jobsList)
            })
        }
        $scope.scheduler.selected = true;
        $scope.$broadcast('scheduler', $scope.scheduler);
    };

    $scope.delete = function (uuid) {
        schedulerService.delete(uuid).then(function (req) {
            $scope.showMessage({content: req.message})
            return $location.path("/app/scheduler");
        });
    }
    $scope.refresh();

}]);

app.controller('SchedulerDetailCtrl', ['$scope', 'schedulerService', '$stateParams', "$state", function ($scope, schedulerService, $stateParams, $state) {
    $scope.$on('scheduler', function (event, data) {
        $scope.scheduler = data;
    });

    $scope.$on('message', function (event, data) {
        $scope.message = data;
    });

    $scope.$on('firstJob', function (event, data) {
        $scope.jobs = data;
    })
    $scope.delete = function (uuid) {
        //console.log("delete的uuid为："+scheduler.name);
        console.log("delete的uuid为：" + uuid);
        schedulerService.delete(uuid).then(function (req) {
            $scope.showMessage({content: req.message})
            //return $location.path("/scheduler/manager");
            $state.go('scheduler.manager');
        });
    }

    $scope.runJobs = function () {
        console.log("runJobsController.$scope.scheduler.name>>>" + $scope.scheduler.uuid);
        schedulerService.runJobs($scope.scheduler.uuid).then(function (req) {
            $scope.showMessage({content: req.message})
            //return $location.path("/scheduler/manager");///app/process/manager
            $state.go('scheduler.manager');
            //return $location.path("/scheduler/manager");
        })
    }
    $scope.shutDownJobs = function(){//关闭调度器
        console.log("shutDownJobs>>>"+$scope.scheduler.name);
        schedulerService.shutDownJobs($scope.scheduler.uuid).then(function(req){
            $scope.showMessage({content: req.message});
            //return $location.path("/scheduler/manager");
            $state.go('scheduler.manager');
        });
    }
    //$scope.refresh();
}]);

app.controller('SchedulerEditCtrl', ['$scope', '$log', '$location', 'schedulerService', '$modal', '$state', '$stateParams', 'dataService', function ($scope, $log, $location, schedulerService, $modal, $state, $stateParams, dataService) {
    //console.log($scope.scheduler);
    //console.info("editUuid?:" + $stateParams.uuid)
    if ($stateParams.uuid != null) {
        schedulerService.get($stateParams.uuid).then(function (data) {
            //console.error("????");
            $scope.scheduler = data;
            $scope.scheduler.success = true;
            //$scope.scheduler.version = schedulerService.getVersion(data.version);
        });
        $scope.$on('scheduler', function (event, data) {
            $scope.scheduler = data;
            $scope.scheduler.success = true;
            //$scope.scheduler.version = schedulerService.getVersion(data.version);
        });
    } else {
        $scope.scheduler = {};
        $scope.scheduler.success = true;
    }


    //$scope.versions = schedulerService.getVersionArrayAll();
    $scope.saveScheduler = function () {
        //console.info("jobid:>>>>>>>>>>>>>>>>>>>>>" + dataService.jobIds);
        var ids = '';
        for (i = 0; i < dataService.jobIds.length; i++) {
            if (i == dataService.jobIds.length - 1) {
                ids += dataService.jobIds[i]
            } else {
                ids += dataService.jobIds[i] + ','
            }
        }
        $scope.scheduler.jobId = ids;
        console.log("scheduler.jobs.id:" + ids)
        schedulerService.save($scope.scheduler).then(function (res) {

            $scope.showMessage({content: res.message})
            $state.go('scheduler.manager');
            //return $location.path("/scheduler/manager");
        });
    };


}]);
app.controller('ModalDemoCtrl', ['$scope', '$modal', '$log', function ($scope, $modal, $log) {
    data = '';
    $scope.refresh();
    $scope.$on('jobitems', function (event, data) {
        data = data;
        //console.log("121-->"+data)
        $scope.open = function (size) {
            var modalInstance = $modal.open({
                templateUrl: 'myModalContent.html',
                controller: 'ModalInstanceCtrl',
                size: size,
                resolve: {
                    datas: function () {
                        return data;
                    }
                }
            });

            modalInstance.result.then(function (selectedItem) {
                $scope.selected = selectedItem;
            }, function () {
            });
        };
    })

}]);

app.controller('ModalInstanceCtrl', ['$scope', '$modalInstance', 'datas', 'dataService', function ($scope, $modalInstance, datas, dataService) {

    var checked = [];
    $scope.items = datas;
    console.info("items>>>>:" + $scope.items);
    $scope.ok = function () {
        dataService.jobIds = checked;
        console.info("checked:" + checked)
        $modalInstance.dismiss('cancel');
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.bind = function (id) {

        if (checked.indexOf(id) != -1) {
            console.log('删除')
            checked.splice(checked.indexOf(id), 1);
        } else {
            console.log('添加')
            checked.push(id);
        }
    }
}])