app.controller('processCtrl', ['$scope', '$location', 'pros', 'jobs', '$stateParams','$timeout','$modal',function ($scope, $location, pros, jobs, $stateParams,$timeout,$modal) {
     $scope.showShellLog = function (data) {
                var modalInstance = $modal.open({
                    templateUrl: 'shellLoglist.html',
                    controller: 'shellLogCtrl',
                    size: '',
                    resolve: {
                        data: function () {
                            return data;
                        }
                    }
                });

                modalInstance.result.then(function () {
                    $scope.refresh();
                }, function () {
                    $log.info('Modal dismissed at: ' + new Date());
                });
            };


    var wc = 2; //执行完成
    var zx = 1; //正在执行
    var init = function(){
     jobs.all().then(function (resp) {
            var jobs;
            if (resp.data.success) {
                jobs = resp.data.list;
                $scope.jobs = jobs;
            } else {
                $scope.showMessage({content: resp.data.message})
            }

        });
    }

    init();

    var interval;

     $scope.startJob = function(jId){
       jobs.start(jId).then(function(resp){
           if(resp.data.success){
               $scope.showMessage(resp.data)
           }
       })
    }

    $scope.getZXJob = function(){
          interval = setInterval(function(){
                pros.list(zx).then(function(resp){
                var zxPros;
                if (resp.data.success) {
                    zxPros = resp.data.list;
                     console.log(zxPros)
                     $scope.zxPros = zxPros;
                } else {
                    $scope.showMessage(resp.data)
                }
             })
          },1000);
    }
    $scope.cleanInterval = function(){
        clearInterval(interval)
    }

     $scope.getWCJob = function(){
            clearInterval(interval)
            pros.list(wc).then(function(resp){
            var wcPros;
            if (resp.data.success) {
                wcPros = resp.data.list;
                  console.log(wcPros)
                  $scope.wcPros = wcPros;
            } else {
                $scope.showMessage(resp.data)
            }
        })
    }

    $scope.getInfo = function(proId){
        pros.get(proId).then(function(resp){
            if (resp.data.success) {
                $scope.showShellLog(resp.data.list);
            } else {
                $scope.showMessage(resp.data)
            }
        })
    }


}]);

app.controller('shellLogCtrl', ['$scope', '$modalInstance','data', function ($scope, $modalInstance, data) {
    $scope.data = data;
    $scope.close = function(){
         $modalInstance.dismiss('cancel');
    }
}]);