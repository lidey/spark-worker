// A RESTful factory for retreiving models from 'models.json'
app.factory('modelService', ['$http', function ($http) {

    var factory = {};

    factory.tree = function () {
        return $http.get('database/model/tree').then(function (resp) {
            return resp.data.tree;
        });
    };

    factory.save_category = function (category) {
        return $http.post('database/category/save', category).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete_category = function (uuid) {
        return $http.get('database/category/remove', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.save_model = function (model) {
        return $http.post('database/model/save', model).then(function (resp) {
            return resp.data;
        });
    };

    factory.get_model = function (uuid) {
        return $http.get('database/' + uuid + '/model').then(function (resp) {
            return resp.data.model;
        });
    };

    factory.delete_model = function (uuid) {
        return $http.get('database/model/remove', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.save_modelTable = function (modelTable) {
        return $http.post('database/modelTable/import', modelTable).then(function (resp) {
            return resp.data;
        });
    };

    factory.table_tree = function (m_uuid) {
        return $http.get('database/model/table_tree', {params: {m_uuid: m_uuid}}).then(function (resp) {
            return resp.data.tree;
        });
    };

    factory.save_modelIndex = function (index) {
        return $http.post('database/index/save', index).then(function (resp) {
            return resp.data;
        });
    };

    factory.modelIndex_list = function (m_uuid) {
        return $http.get('database/' + m_uuid + '/index_list').then(function (resp) {
            return resp.data.indexes;
        });
    };


    factory.delete_index = function (uuid) {
        return $http.get('database/index/remove', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    return factory;
}]);