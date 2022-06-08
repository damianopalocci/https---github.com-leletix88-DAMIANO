myapp.controller("last_lettureController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('last_lettureController');



        $http.get("/rs/last_letture").then(function(resp) {
            $scope.last_letture = resp.data
            console.log($scope.last_letture)
            $scope.totalItems = $scope.last_letture.length;
        })

        $scope.totalItems = 0
        $scope.currentPage = 1;
        $scope.numPerPage = 15;




        $scope.paginate = function(value) {
            var begin, end, index;
            begin = ($scope.currentPage - 1) * $scope.numPerPage;
            end = begin + $scope.numPerPage;
            index = $scope.last_letture.indexOf(value);
            return (begin <= index && index < end);
        };





    }





]);