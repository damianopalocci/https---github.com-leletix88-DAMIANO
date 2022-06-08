myapp.controller("tipo_lavorazioneController", [
    "$scope", "$rootScope", "$http", "$routeParams", "$location", "$routeParams",

    function($scope, $rootScope, $http, $routeParams, $location) {
        // create a message 
        console.log('tipo_lavorazioneController');

        $scope.articoid = $routeParams.id;

        $http.get('officina/lavorazione/get_codice/' + $scope.articoid).then(function(resp) {
            $scope.db_principale = resp.data[0]
            console.log($scope.db_principale)
        });




    }
]);