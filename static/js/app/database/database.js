app.controller('DatabaseCtrl', ['$scope', 'databaseService', '$timeout', function ($scope, databaseService, $timeout) {
    var tree;
    $scope.my_data = [];
    $scope.my_tree = tree = {};
    $scope.reload = function () {
        $scope.my_data = [];
        var data_root = {
            uid: 'root',
            label: '数据库链接',
            icon: 'fa fa-folder-o'
        };
        databaseService.tree().then(function (data) {
            data_root.children = data;
            $scope.my_data = [data_root];
        });
        $scope.doing_async = true;
        return $timeout(function () {
            $scope.doing_async = false;
            return tree.expand_all();
        }, 1000);
    };
    $scope.my_tree_handler = function (branch) {
        if (branch.type != null) {
            $scope.title = branch.label;
            $scope.$broadcast('branch', branch);
        }
    };

}]);

app.controller('DatabaseIndexCtrl', ['$scope', 'databaseService', '$stateParams', '$modal', function ($scope, databaseService, $stateParams, $modal) {
    $scope.database_detail = false;
    $scope.database_table = false;
    $scope.$on('branch', function (event, branch) {
        if (branch.type == 'database') {
            $scope.database = branch.data;
            $scope.database_detail = true;
            $scope.database_table = false;
        }
        if (branch.type == 'group') {
            $scope.database_detail = false;
            $scope.database_table = true;

        }
    });

    $scope.testDatabase = function () {
        databaseService.test($scope.database.uuid).then(function (data) {
            $scope.showMessage(data);
        });
    };
}]);

app.controller('DatabaseEditCtrl', ['$scope', 'databaseService', '$state', '$stateParams', function ($scope, databaseService, $state, $stateParams) {

}]);

app.controller('DatabaseConfirmCtrl', ['$scope', '$modalInstance', '$timeout', 'message', function ($scope, $modalInstance, $timeout, message) {
    $scope.message = {content: message};

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.ok = function () {
        $modalInstance.close('delete');
    };
}]);
