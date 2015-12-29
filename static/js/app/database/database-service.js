// A RESTful factory for retreiving databases from 'databases.json'
app.factory('databaseService', ['$http', function ($http) {

    var factory = {};

    var databases;

    var typeArray = [
        {name: 'Mysql', key: 'Mysql'}
    ];

    factory.tree = function () {
        databases = $http.get("database/tree").then(function (resp) {
            return resp.data.tree;
        });
        return databases;
    };

    factory.test = function (uuid) {
        return $http.get("database/test", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.all = function () {
        databases = $http.get("database/list").then(function (resp) {
            return resp.data.databases;
        });
        return databases;
    };

    factory.save = function (database) {
        return $http.post("database/save", database).then(function (resp) {
            return resp.data;
        });
    };

    factory.get = function (uuid) {
        return $http.get("database/info", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete = function (uuid) {
        return databases = $http.get("database/remove", {params: {uuid: uuid}}).then(function (resp) {
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