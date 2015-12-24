// A RESTful factory for retreiving mails from 'mails.json'
app.factory('schedulerService', ['$http', function ($http) {
  //var path = 'static/js/app/scheduler/scheduler.json';
  /*var path = 'scheduler/list';
  var schedulers = $http.get(path).then(function (resp) {
    console.info(resp.data.list);
    return resp.data.list;
  });*/

  var factory = {};
    var schedulers;
  factory.all = function () {
    /*var path = "scheduler/list";
    var list = ''
      return  $http.get(path).then(function (resp) {
             list = resp.data.list
             return list;
      })*/
      schedulers = $http.get("scheduler/list").then(function (resp) {
            return resp.data.list;
        });
        return schedulers;
  };
   factory.save = function (scheduler) {
        return $http.post("scheduler/save", scheduler).then(function (resp) {
            return resp.data;
        });
    };

    factory.get = function (uuid) {
        return $http.get("scheduler/getUUID", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete = function (uuid) {
        return schedulers = $http.get("scheduler/delete", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };
    factory.runJobs = function (uuid){
        return $http.get("scheduler/runJobs",{params:{uuid: uuid}}).then(function(resp){
            return resp.data;
        });
    }
    factory.shutDownJobs= function (uuid){
        return $http.get("scheduler/shutDownJobs",{params: {uuid: uuid}}).then(function(resp){
            return resp.data;
        })
    }
factory.uuid =  function () {
    function S4() {
       return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    }
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}
  return factory;
}]);