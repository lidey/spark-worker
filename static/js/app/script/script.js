app.controller('ScriptListCtrl', ['$scope', '$location', 'scripts', '$state', 'dataService', '$stateParams', function ($scope, $location, scripts, $state, dataService, $stateParams) {
    $scope.jobId = $stateParams.jobId
    var jobs = dataService.data;

    for (var i = 0; i < jobs.length; i++) {
        if (jobs[i].id == $stateParams.jobId) {
            jobs[i].selected = true;
        } else {
            jobs[i].selected = false;
        }
    }
    dataService.data = jobs;

    scripts.all($stateParams.jobId).then(function (resp) {
        var scripts;
        if (resp.data.success) {
            scripts = resp.data.list;
        } else {
            $scope.showMessage({content: resp.data.message})
        }
        $scope.scripts = scripts;
    });

    $scope.addScript = function (jobId) {
        return $location.path("/app/job/script/add/" + jobId);
    }
    $scope.deleteScript = function (scriptId) {
        scripts.delete(scriptId).then(function (resp) {
            if (resp.data.success) {
                $scope.showMessage({content: resp.data.message})
            } else {
                $scope.showMessage({content: resp.data.message})
            }
        })
        return $location.path("/app/job/info/" + jobId);
    }

    $scope.editJob = function (jobId) {
        return $location.path("/app/job/info/" + jobId);
    }

}]);


app.controller('ScriptNewCtrl', ['$scope', '$location', '$http', 'scripts', '$state', '$stateParams', function ($scope, $location, $http, scripts, $state, $stateParams) {
    $scope.script = {
        id: "",
        title: "",
        script: "",
        date: Date.now(),
        server_id: "",
        job_id: $stateParams.jobId
    }
    scripts.all_server().then(function (servers) {
        $scope.servers = servers;
        console.info($scope.servers)
    });

    $scope.saveScript = function () {
        $scope.script.id = scripts.uuid()
        scripts.add($scope.script).then(function (resp) {
            if (resp.data.success) {
                $scope.showMessage({content: resp.data.message})
            } else {
                $scope.showMessage({content: resp.data.message})
            }
        })
        return $location.path("/app/job/script/list/" + $stateParams.jobId);
    }

}]);

app.controller('ScriptInfoCtrl', ['$scope', '$location', '$http', 'scripts', '$state', '$stateParams', function ($scope, $location, $http, scripts, $state, $stateParams) {
    $scope.editFlag = false

    scripts.get($stateParams.scriptId).then(function (resp) {
        $scope.script = resp.data.script;

        scripts.all_server().then(function (servers) {
            $scope.servers = servers;

            if ($scope.servers != null) {
                for (var i = 0; i < $scope.servers.length; i++) {
                    if ($scope.servers[i].uuid == $scope.script.server_id) {
                        $scope.servers[i].selected = true;
                    } else {
                        $scope.servers[i].selected = false;
                    }
                }
            }
        });
    })


    $scope.editScript = function () {
        $scope.editFlag = true;
    }
    $scope.saveScript = function () {
        scripts.update($scope.script).then(function (resp) {
            if (resp.data.success) {
                $scope.showMessage({content: resp.data.message})
            } else {
                $scope.showMessage({content: resp.data.message})
            }
        })
        return $location.path("/app/job/script/list/" + $scope.script.job_id);
    }

    $scope.deleteScript = function (scriptId) {
        scripts.delete(scriptId).then(function (resp) {
            if (resp.data.success) {
                $scope.showMessage({content: resp.data.message})
            } else {
                $scope.showMessage({content: resp.data.message})
            }
        })
        return $location.path("/app/job/script/list/" + $scope.script.job_id);
    }

}]);
