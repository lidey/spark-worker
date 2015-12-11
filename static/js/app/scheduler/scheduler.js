app.controller('SchedulerCtrl', ['$scope','schedulerService', '$http', function($scope,schedulerService, $http) {
    /*var schedulers;
    schedulers.all().then(function(req){
        *//*if(req.data.success){
            schedulers = req.data.list;
        }*//*
        console.info("schedulers:"+req);
        $scope.schedulers = req;
        $scope.scheduler = $scope.schedulers[0];
        $scope.schedulers[0].selected = true;
        console.info("schedulerID:"+$scope.schedulers[0].uuid)

    });
    $scope.colors = ['primary', 'info', 'success', 'warning', 'danger', 'dark'];*/
    $scope.refresh = function () {
        schedulerService.all().then(function (req) {
            $scope.schedulers = req;
            if ($scope.scheduler == undefined)
                $scope.scheduler = $scope.schedulers[0];
            else
                angular.forEach($scope.schedulers, function (reqs) {
                    if (reqs.uuid == $scope.scheduler.uuid)
                        reqs.selected = true;
                });
            $scope.scheduler.selected = true;
            $scope.$broadcast('scheduler', $scope.scheduler);
        });
    };


  $scope.selectScheduler = function (scheduler) {
        angular.forEach($scope.schedulers, function (scheduler) {
            scheduler.selected = false;
        });
        $scope.scheduler = scheduler;
        $scope.scheduler.selected = true;
        $scope.$broadcast('scheduler', $scope.scheduler);
    };


    $scope.refresh();

}]);

app.controller('SchedulerDetailCtrl', ['$scope', 'schedulerService', '$stateParams', function ($scope, schedulerService, $stateParams) {

    $scope.$on('scheduler', function (event, data) {
        $scope.scheduler = data;
        //$scope.server.version = serverService.getVersion(data.version);
    });

    $scope.$on('message', function (event, data) {
        $scope.message = data;
    });

    $scope.delete = function (scheduler) {
        console.log(scheduler);
        schedulerService.delete(scheduler.uuid).then(function (message) {
            $scope.showMessage(message)
        });
    }
}]);

app.controller('SchedulerEditCtrl', ['$scope', '$location', 'schedulerService', '$state', '$stateParams', function ($scope, $location, schedulerService, $state, $stateParams) {
    //console.log($scope.scheduler);
    console.info("uuid?:"+$stateParams.uuid)
    if ($stateParams.uuid != null) {
        schedulerService.get($stateParams.uuid).then(function (data) {
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
        console.info(">>>>>>>>>>>>>>>>>>>>>"+$scope.scheduler.cron);
        schedulerService.save($scope.scheduler).then(function (res) {
            //$scope.showMessage(res.data.message)
            $scope.showMessage({content: res.message})
            $state.go('scheduler.manager');
            //return $location.path("/app/scheduler/manager");
        });
    };

}]);