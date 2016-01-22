// A RESTful factory for retreiving sparks from 'sparks.json'
app.factory('sparkService', ['$http', function ($http) {

    var factory = {};

    var sparks;

    factory.all = function () {
        sparks = $http.get("spark/list").then(function (resp) {
            return resp.data.sparks;
        });
        return sparks;
    };

    factory.job_all = function () {
        return $http.get("spark/job/all").then(function (resp) {
            return resp.data.jobs;
        });
    };

    factory.get = function (uuid) {
        return $http.get("spark/info", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.save_job = function (job) {
        if (job.class != null) {
            job.main_class = job.class.name;
            job.main_jar = job.class.jar;
        }
        return $http.post("spark/job/save", job).then(function (resp) {
            return resp.data;
        });
    };

    factory.get_job = function (uuid) {
        return $http.get("spark/job/info", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete_job = function (uuid) {
        return $http.get("spark/job/remove", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.remove_jar = function (uuid, file_name) {
        return $http.get("spark/job/remove_jar", {
            params: {
                uuid: uuid,
                file_name: file_name
            }
        }).then(function (resp) {
            return resp.data;
        });
    };

    factory.open_jars = function (uuid) {
        return $http.get("spark/job/open_jars", {
            params: {
                uuid: uuid
            }
        }).then(function (resp) {
            return resp.data.classes;
        });
    };

    factory.run_spark = function (uuid) {
        return $http.get("spark/job/start", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.get_log = function (uuid) {
        return $http.get("spark/job/log", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.kill_job = function (uuid) {
        return $http.get("spark/job/kill", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    return factory;
}]);