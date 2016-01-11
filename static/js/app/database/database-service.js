// A RESTful factory for retreiving databases from 'databases.json'
app.factory('databaseService', ['$http', function ($http) {

    var factory = {};

    factory.tree = function () {
        return $http.get('database/tree').then(function (resp) {
            return resp.data.tree;
        });
    };

    factory.test = function (uuid) {
        return $http.get('database/test', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.save_folder = function (folder) {
        return $http.post('database/folder/save', folder).then(function (resp) {
            return resp.data;
        });
    };

    factory.database_list = function () {
        return $http.get('database/database/list').then(function (resp) {
            return resp.data.databases;
        });
    };

    factory.folder_list = function (d_uuid) {
        return $http.get('database/' + d_uuid + '/folder_list').then(function (resp) {
            return resp.data.folders;
        });
    };

    factory.save_database = function (database) {
        return $http.post('database/save', database).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete_database = function (uuid) {
        return $http.get('database/remove', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete_folder = function (uuid) {
        return $http.get('database/folder/remove', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.table_name_list = function (uuid) {
        return $http.get('database/' + uuid + '/table_names', {params: {name: ''}}).then(function (resp) {
            return resp.data.table_names;
        });
    };

    factory.import_tables = function (table) {
        return $http.post('database/' + table.db_uuid + '/import_tables', table).then(function (resp) {
            return resp.data;
        });
    };

    factory.table_list = function (folder) {
        var folder_uuid = '';
        if (folder.type == 'folder')
            folder_uuid = folder.data.uuid;
        return $http.get('database/' + folder.data.db_uuid + '/table_list', {params: {folder_uuid: folder_uuid}}).then(function (resp) {
            return resp.data.tables;
        });
    };

    factory.delete_table = function (uuid) {
        return $http.get('database/table/remove', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete_column = function (uuid) {
        return $http.get('database/column/remove', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };
    factory.column_reload = function (uuid) {
        return $http.get('database/' + uuid + '/reload').then(function (resp) {
            return resp.data;
        });
    };

    return factory;
}]);