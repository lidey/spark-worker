// A RESTful factory for retreiving mails from 'mails.json'
app.factory('jobs', ['$http', function ($http) {

  var factory = {};
  factory.all = function () {
      var path = 'job/list';
      var list = ''
      return  $http.get(path).then(function (resp) {
             list = resp.data.list
             console.info(list)
             return list;
      })
  };
  factory.get = function (id) {

      var path = 'job/getUUID';
      var job;
      return  $http.post(path,{'id':id}).then(function (resp) {
             job = resp.data.job
             console.info(job)
             return job;
      })

  };

    factory.delete = function (id) {
      var path = 'job/deleteUUID';
      var job;
      return  $http.post(path,{'id':id}).then(function (resp) {
             job = resp.data.job
             console.info(job)
             return job;
      })
  };
    factory.add = function (job) {
      return   $http.post('job/add',job).then(function (resp) {
                console.log(resp.data.job)
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