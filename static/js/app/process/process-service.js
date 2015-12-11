// A RESTful factory for retreiving mails from 'mails.json'
app.factory('pros', ['$http', function ($http) {

    var factory = {};

    factory.list = function(status){
          var path = 'process/list';
          return  $http.post(path,{'status':status}).then(function (resp) {
              return resp;
      })

    }


    factory.uuid = function () {
        function S4() {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        }

        return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
    }
    return factory;
}]);