// A RESTful factory for retreiving mails from 'mails.json'
app.factory('pros', ['$http','$rootScope', function ($http,$rootScope) {

    var factory = {};
    var webs;

    factory.get = function(proID){
          var path = 'process/get';
          return  $http.post(path,{'pro_id':proID}).then(function (resp) {
              return resp;
      })

    }

    factory.list = function(status){
          var path = 'process/list';
          return  $http.post(path,{'status':status}).then(function (resp) {
              return resp;
      })

    }
    factory.sorket = function(){
       webs = new WebSocket('ws://localhost:8880/job-socket');
            webs.onmessage = function(event) {
                   console.log('onmessage')
                 console.log(eval('('+event.data+')').type)
                 var type = eval('('+event.data+')').type;
                if(type=='all'){
                      $rootScope.$broadcast('list',eval('('+event.data+')').list)
                }else{
                      $rootScope.$broadcast('zxz', eval('('+event.data+')').progress)
                }



           };
        webs.onopen = function(event) {
            console.log("onopen")
           };

    }
    factory.colse = function(){
        if(webs != null){
             webs.close()
             webs = null;
        }

    }
    factory.uuid = function () {
        function S4() {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        }

        return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
    }
    return factory;
}]);