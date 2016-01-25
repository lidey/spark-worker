// A RESTful factory for retreiving servers from 'servers.json'
app.factory('serverService', ['$http', function ($http) {

    var factory = {};

    var versionArray = [
        {name: 'CentOS 7 以上版本', key: 'CentOS-7', type: 'Linux'},
        {name: 'CentOS 6 以上版本', key: 'CentOS-6', type: 'Linux'},
        {name: 'Window 2008', key: 'Window-2008', type: 'Window'}
    ];

    factory.tree = function () {
        return $http.get("server/folder/tree").then(function (resp) {
            return resp.data.tree;
        });
    };

    factory.all = function () {
        return $http.get("server/all").then(function (resp) {
            return resp.data.servers;
        });
    };

    factory.folder_save = function (folder) {
        return $http.post("server/folder/save", folder).then(function (resp) {
            return resp.data;
        });
    };

    factory.folder_get = function (uuid) {
        return $http.get("server/folder/info", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.folder_delete = function (uuid) {
        return $http.get("server/folder/remove", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.save = function (server) {
        console.log(server)
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
        return $http.get("server/remove", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.test = function (uuid) {
        return $http.get("server/test", {params: {uuid: uuid}}).then(function (resp) {
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