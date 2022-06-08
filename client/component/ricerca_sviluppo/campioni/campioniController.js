myapp.controller("campioniController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('campioniController');






        $http.get('/tools/campioni/getcampioni/getsum').then(function(resp) {
            $scope.db_tipo = resp.data


            $scope.current_page = $location.path()
            let look_path = $scope.current_page.split('/')
            $scope.current_page = look_path[2]


            angular.forEach($scope.db_tipo, function(value) {
                if (value._id == 'Vending') {
                    $scope.totvending = value.count
                }
                if (value._id == 'Tradizionale') {
                    $scope.tottradizionale = value.count
                }

                $scope.campioni_tot = $scope.tottradizionale + $scope.totvending
            });



        });




    }
]);