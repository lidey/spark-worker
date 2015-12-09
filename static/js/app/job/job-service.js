// A RESTful factory for retreiving mails from 'mails.json'
app.factory('jobs', ['$http',function ($http) {

  var factory = {};
  factory.all = function () {
      var path = 'job/list';
      var list = ''
      return  $http.get(path).then(function (resp) {
          return resp;
      })
  };
    factory.script_all = function (job_id) {
      var path = 'script/list';
      var list = ''
      return  $http.post(path,{'job_id':job_id}).then(function (resp) {
          return resp;

      })
  };
  factory.get = function (id) {
      var path = 'job/getUUID';
      var job;
      return  $http.post(path,{'id':id}).then(function (resp) {
          return resp;
      })

  };

    factory.delete = function (id) {
      var path = 'job/deleteUUID';
      var job;
      return  $http.post(path,{'id':id}).then(function (resp) {
           return resp;
      })
  };
    factory.add = function (job) {
      return   $http.post('job/add',job).then(function (resp) {
               return resp;
            });
  };

    factory.update = function (job) {
      return   $http.post('job/update',job).then(function (resp) {
                return resp;
            });
  };

   factory.uuid =  function () {
    function S4() {
       return (((1+Math.random())*0x10000)|0).toString(16).substring(1);
    }
    return (S4()+S4()+"-"+S4()+"-"+S4()+"-"+S4()+"-"+S4()+S4()+S4());
}
  return factory;
}]);