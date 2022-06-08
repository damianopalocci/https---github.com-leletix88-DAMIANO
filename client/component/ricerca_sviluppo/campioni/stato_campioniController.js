myapp.controller("stato_campioniController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('stato_campioniController');




        $scope.ulrp = $routeParams.tipo;
        $scope.stato = $routeParams.stato;
        if ($scope.ulrp == 'tradizionale') {
            q = 'Tradizionale'
        } else { q = 'Vending' }


        $http.get('/tools/campioni/getcampioni/' + q + '/' + $scope.stato).then(function(resp) {
            $scope.db_tipo = resp.data

            $rootScope.current_page = $location.path()
            $rootScope.current_page = $rootScope.current_page.split('/')
            $rootScope.current_page = $rootScope.current_page[4]

        });



        $scope.deleteoneid = function(id) {
            x = confirm("Vuoi eliminare l'artico selezionato " + id)
            id = String(id)
            if (x == true) {
                $http.get('/tools/campioni/delete/' + id).then(function(resp) {
                    $scope.msg_delete = resp.data
                    if ($scope.msg_delete.msg == 200) {
                        $http.get('/tools/campioni/getcampioni/' + q + '/' + $scope.stato).then(function(resp) {
                            $scope.db_tipo = resp.data
                            $scope.$apply()
                        });
                    }
                });
            }
        }







    }
]);