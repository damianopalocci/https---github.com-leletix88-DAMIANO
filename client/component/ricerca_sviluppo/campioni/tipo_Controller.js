myapp.controller("tipo_Controller", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('tipo_Controller');




        $scope.url = $routeParams.tipo

        if ($scope.url == 'tradizionale') {

            $scope.color = "#313135";
            q = 'Tradizionale';
        } else {
            $scope.color = "#023e7d";
            q = 'Vending';
        }


        $http.get('/tools/campioni/getcampioni/getsum/' + q).then(function(resp) {
            $scope.lista = resp.data

            $rootScope.current_page = $location.path()
            $rootScope.current_page = $rootScope.current_page.split('/')
            $rootScope.current_page = $rootScope.current_page[3]

        });



    }
]);