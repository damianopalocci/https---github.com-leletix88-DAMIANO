myapp.controller("campioni_tradizionaleController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('campioni_tradizionaleController');


        $http.get('/tools/campioni/getcampioni/Tradizionale').then(function(resp) {
            $scope.db_tipo = resp.data
        });





        $scope.lista = [{ 'qta': 3, 'titolo': 'in attesa' }, { 'qta': 23, 'titolo': 'ciaso cioa ' }, { 'qta': 50, 'titolo': 'bla bla ' }]

    }
]);