myapp.controller("dashboard_adminController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('dashboard_adminController');

        $scope.current_page = $location.path()
        let look_path = $scope.current_page.split('/')
        console.log(look_path)
        $scope.current_page = look_path[1]


    }
]);