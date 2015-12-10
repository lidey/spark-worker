// A RESTful factory for retreiving mails from 'mails.json'
app.factory('scripts', ['$http', function ($http) {

    var factory = {};
    factory.all = function (job_id) {
        var path = 'script/list';
        var list = ''
        return $http.post(path, {'job_id': job_id}).then(function (resp) {
            return resp;

        })
    };
    factory.get = function (id) {
        var path = 'script/get';
        var script;
        return $http.post(path, {'id': id}).then(function (resp) {
            return resp;
        })

    };

    factory.delete = function (id) {
        var path = 'script/remove';
        var script;
        return $http.post(path, {'id': id}).then(function (resp) {
            return resp;
        })
    };
    factory.add = function (script) {
        return $http.post('script/save', script).then(function (resp) {
            return resp;
        });
    };

    factory.update = function (script) {
        return $http.post('script/update', script).then(function (resp) {
            return resp;
        });
    };

    factory.all_server = function () {
        servers = $http.get("server/list").then(function (resp) {
            return resp.data.servers;
        });
        return servers;
    };
    factory.test = function (script) {
        return $http.post('script/test', script).then(function (resp) {
            return resp;
        });
    };


    factory.uuid = function () {
        function S4() {
            return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
        }

        return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
    }
    return factory;
}]);