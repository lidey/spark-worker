// A RESTful factory for retreiving mails from 'mails.json'
app.factory('schedulerService', ['$http', function ($http) {

    var factory = {};

    factory.save = function (scheduler) {
        scheduler.job_uuid = scheduler.job.uuid;
        return $http.post("scheduler/save", scheduler).then(function (resp) {
            return resp.data;
        });
    };

    factory.set_cron = function (cron) {
        return $http.post("scheduler/set_cron", cron).then(function (resp) {
            return resp.data;
        });
    };

    factory.get = function (uuid) {
        return $http.get("scheduler/info", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.delete = function (uuid) {
        return schedulers = $http.get("scheduler/delete", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.startup = function (uuid) {
        return $http.get("scheduler/startup", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    factory.shutdown = function (uuid) {
        return $http.get("scheduler/shutdown", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        })
    };

    factory.get_log = function (uuid) {
        return $http.get("scheduler/log", {params: {uuid: uuid}}).then(function (resp) {
            return resp.data;
        });
    };

    return factory;
}]);