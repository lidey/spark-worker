app.controller('JobCtrl', ['$rootScope','$scope','$location', 'jobs','dataService' ,'$stateParams', function ($rootScope,$scope,$location, jobs ,dataService,$stateParams) {

    $scope.colors = ['primary', 'info', 'success', 'warning', 'danger', 'dark'];
    var jId;
    jobs.all().then(function (jobs) {

        $scope.jobs = jobs;
        jId = jobs[0].id
        dataService.data = jobs;
        //$scope.jobs[0].selected = true;

    });
    jobs.script_all(jId);
    $scope.deleteJob = function (jobId) {
        console.info('删除'+jobId)
        jobs.delete(jobId)
        for (var i = 0; i < $scope.jobs.length; i++) {
             if ($scope.jobs[i].id == jobId)
             $scope.jobs.splice(i,1);
        }
        return $location.path("/app/job");
    }



}]);

app.controller('JobDetailCtrl', ['$scope','$location', 'jobs', '$stateParams','dataService', function ($scope,$location, jobs, $stateParams,dataService) {
    console.info('查询--'+$stateParams.id)
    jobs.get($stateParams.id).then(function (job) {
        $scope.job = job;
        console.info(job)
    })
    if( $scope.jobs!=null){
            for (var i = 0; i < $scope.jobs.length; i++) {
             if ($scope.jobs[i].id == $stateParams.id)
              $scope.jobs[i].selected =true;
             else
             $scope.jobs[i].selected =false;
        }
    }

    $scope.editJob = function(){
         jobs.update($scope.job)

         for (var i = 0; i < $scope.jobs.length; i++) {
             if ($scope.jobs[i].id == $scope.job.id){
                  $scope.jobs[i] = $scope.job;
                  $scope.jobs[i].selected =true;
                    console.info($scope.jobs[i])
             } else{
                  $scope.jobs[i].selected =false;
             }
         }
         return $location.path("/app/job/add");
    }




}]);

app.controller('JobNewCtrl', ['$scope','$location','$http','jobs', function ($scope,$location,$http,jobs) {
    $scope.job={
        id:"",
        title:"",
        content:"",
        date:Date.now()
    }
    $scope.saveJob = function(){
        $scope.job.id = jobs.uuid()

        $scope.jobs.push($scope.job)

        jobs.add($scope.job)

        for (var i = 0; i < $scope.jobs.length; i++) {
                     $scope.jobs[i].selected =false;
                }
        return $location.path("/app/job/script/list/"+$scope.job.id);

    }





}]);
