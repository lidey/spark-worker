// A RESTful factory for retreiving mails from 'mails.json'
app.factory('jobs', ['$http','commAlertService',function ($http,commAlertService) {

  var factory = {};
  factory.all = function () {
      var path = 'job/list';
      var list = ''
      return  $http.get(path).then(function (resp) {
          if(resp.data.success){
             list = resp.data.list;
              console.log(resp.data.message)
              return list;
          }else{
              console.error(resp.data.message)
              return null;
          }

      })
  };
  factory.get = function (id) {
      var path = 'job/getUUID';
      var job;
      return  $http.post(path,{'id':id}).then(function (resp) {
          if(resp.data.success){
              job = resp.data.job
              console.log(resp.data.message)
              return job;
          }else{
              console.error(resp.data.message)
              return null;
          }

      })

  };

    factory.delete = function (id) {
      var path = 'job/deleteUUID';
      var job;
      return  $http.post(path,{'id':id}).then(function (resp) {
          if(resp.data.success){
              job = resp.data.job
              console.log(resp.data.message)
              return job;
          }else{
              console.error(resp.data.message)
              return null;
          }

      })
  };
    factory.add = function (job) {
      return   $http.post('job/add',job).then(function (resp) {
              if(resp.data.success){
                  console.log(resp.data.message)
              }else{
                  console.error(resp.data.message)
              }
            });
  };

    factory.update = function (job) {
      return   $http.post('job/update',job).then(function (resp) {
                if(resp.data.success){
                  console.log(resp.data.message)
                  }else{
                      console.error(resp.data.message)
                  }
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