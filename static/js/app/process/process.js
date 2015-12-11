app.controller('processCtrl', ['$scope', '$location', 'pros', 'jobs', '$stateParams','$timeout',function ($scope, $location, pros, jobs, $stateParams,$timeout) {
    var wc = 2; //执行完成
    var zx = 1; //正在执行

    var refresh = function(){
     jobs.all().then(function (resp) {
            var jobs;
            if (resp.data.success) {
                jobs = resp.data.list;
                $scope.jobs = jobs;
            } else {
                $scope.showMessage({content: resp.data.message})
            }

        });
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
    }
      refresh();
     /* setInterval(function(){
           refresh();
      },5000);*/
     $scope.startJob = function(jId){
       jobs.start(jId).then(function(resp){
           if(resp.data.success){
               $scope.showMessage(resp.data)
           }
       })
    }


}]);
