app.controller('processCtrl', ['$scope', '$location', 'pros', 'jobs', '$stateParams','$timeout','$modal',function ($scope, $location, pros, jobs, $stateParams,$timeout,$modal) {

    $scope.zxPros = []; //执行中任务数组
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
            };

     pros.sorket();
     $scope.$on('list', function (event, data) {
         $scope.zxPros = data;
           $scope.$apply()
     })
    var getWCJob =  function(){
            pros.list(wc).then(function(resp){
            var wcPros;
            if (resp.data.success) {
                wcPros = resp.data.list;
                  console.log(wcPros)
                  $scope.wcPros = wcPros;
                    $scope.pageSize = 10;
                  $scope.curPage = 1;
                  $scope.pageCount = Math.ceil($scope.wcPros.length / $scope.pageSize) - 1
                    $scope.totalCount = $scope.wcPros.length;
            } else {
                $scope.showMessage(resp.data)
            }
        })


    }

    $scope.$on('zxz', function (event, data) {
          console.log(data)
          if(data.status == '执行完成'){
              for(var i=0;i<$scope.zxPros.length;i++){
                       if( $scope.zxPros[i].id == data.id){
                           $scope.zxPros.splice($scope.zxPros.indexOf($scope.zxPros[i]), 1);
                           getWCJob();
                       }
                  }

          }else{
              if($scope.zxPros.length>0){
                   var cFlag = false;
                   for(var i=0;i<$scope.zxPros.length;i++){
                       if( $scope.zxPros[i].id == data.id){
                           $scope.zxPros[i]=data;
                           //$scope.zxPros[i].fail_num = data.fail_num;
                           cFlag = true;
                       }
                  }
                   if(!cFlag){
                       $scope.zxPros.push(data)
                   }
              }else{
                    $scope.zxPros.push(data)
              }
          }
          $scope.$apply()
        })
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
        getWCJob();
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

    //$scope.getZXJob = function(){
    //      interval = setInterval(function(){
    //            pros.list(zx).then(function(resp){
    //            var zxPros;
    //            if (resp.data.success) {
    //                zxPros = resp.data.list;
    //                 console.log(zxPros)
    //                 $scope.zxPros = zxPros;
    //            } else {
    //                $scope.showMessage(resp.data)
    //            }
    //         })
    //      },1000);
    //}
    $scope.cleanInterval = function(){
        //clearInterval(interval)
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


app.filter('pageStartFrom', [function() {
  return function(input, start) {
        start = +start;
    return input.slice(start);
  }
}]);