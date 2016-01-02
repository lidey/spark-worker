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

    factory.delete_model = function (uuid) {
        return $http.get('database/model/remove', {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    return factory;
}]);