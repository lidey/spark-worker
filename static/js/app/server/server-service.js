// A RESTful factory for retreiving servers from 'servers.json'
app.factory('serverService', ['$http', function ($http) {

    var factory = {};

    var servers;

    var versionArray = [
        {name: 'CentOS 7 以上版本', key: 'CentOS-7', type: 'Linux'},
        {name: 'CentOS 6 以上版本', key: 'CentOS-6', type: 'Linux'},
        {name: 'Window 2008', key: 'Window-2008', type: 'Window'}
    ];

    factory.all = function () {
        servers = $http.get("server/list").then(function (resp) {
            return resp.data.servers;
        });
        return servers;
    };

    factory.save = function (server) {
        return $http.post("server/save", server).then(function (resp) {
            return resp.data;
        });
    };

    factory.get = function (uuid) {
        return $http.get("server/info", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete = function (uuid) {
        return servers = $http.get("server/remove", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.test = function (server) {
        return servers = $http.post("server/test", server).then(function (resp) {
            return resp.data;
        });
    };

    factory.getVersionArrayAll = function () {
        return versionArray;
    };

    factory.getVersion = function (key) {
        var version = key;
        angular.forEach(versionArray, function (tmp) {

            if (tmp.key == key) {
                version = tmp;
            }
        });
        return version;
    };

    return factory;
}]);